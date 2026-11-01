const express = require('express');
const router = express.Router();
const Stripe = require('stripe');
const db = require('../db');
const { requireAuth, optionalAuth, verifySessionJwt } = require('../auth');
const { sendPaymentSuccessEmail, sendPaymentFailedEmail } = require('../email');
const { getPricing } = require('../pricing');

const rawStripeKey = (process.env.STRIPE_SECRET_KEY || 'PLACEHOLDER').trim();
const stripeAccountId = (process.env.STRIPE_ACCOUNT_ID || 'acct_1URD6NFTOW7EuxVG').trim();
const hasRealStripeKey = (
  rawStripeKey.startsWith('sk_') ||
  rawStripeKey.startsWith('oak_') ||
  rawStripeKey.startsWith('rk_')
) && rawStripeKey !== 'sk_test_placeholder';

const stripeOptions = {};
if (rawStripeKey.startsWith('oak_') || stripeAccountId) {
  stripeOptions.stripeAccount = stripeAccountId;
}
const stripe = new Stripe(hasRealStripeKey ? rawStripeKey : 'sk_test_mock_for_hmac', stripeOptions);

// Auto-initialize billing and accounting ledger tables
async function initBillingTables() {
  try {
    await db.query(`
      CREATE TABLE IF NOT EXISTS payment_transactions (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        user_id UUID REFERENCES users(id) ON DELETE SET NULL,
        stripe_session_id TEXT UNIQUE,
        stripe_payment_intent TEXT UNIQUE,
        stripe_charge_id TEXT,
        tier TEXT NOT NULL DEFAULT 'STANDARD',
        gross_amount_cents INTEGER NOT NULL,
        discount_amount_cents INTEGER NOT NULL DEFAULT 0,
        rush_amount_cents INTEGER NOT NULL DEFAULT 0,
        stripe_fee_cents INTEGER DEFAULT 0,
        net_amount_cents INTEGER NOT NULL,
        currency TEXT NOT NULL DEFAULT 'usd',
        coupon_id UUID REFERENCES coupons(id) ON DELETE SET NULL,
        coupon_code TEXT,
        partnership_id UUID REFERENCES partnerships(id) ON DELETE SET NULL,
        status TEXT NOT NULL DEFAULT 'PENDING',
        customer_email TEXT NOT NULL,
        customer_name TEXT,
        payment_method_type TEXT,
        receipt_url TEXT,
        refund_amount_cents INTEGER DEFAULT 0,
        refunded_at TIMESTAMPTZ,
        stripe_refund_id TEXT,
        metadata JSONB,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
      );
      CREATE INDEX IF NOT EXISTS idx_payment_tx_user ON payment_transactions(user_id);
      CREATE INDEX IF NOT EXISTS idx_payment_tx_status ON payment_transactions(status);
      CREATE INDEX IF NOT EXISTS idx_payment_tx_session ON payment_transactions(stripe_session_id);
      CREATE INDEX IF NOT EXISTS idx_payment_tx_intent ON payment_transactions(stripe_payment_intent);
      CREATE INDEX IF NOT EXISTS idx_payment_tx_created ON payment_transactions(created_at DESC);

      CREATE TABLE IF NOT EXISTS processed_stripe_events (
        event_id TEXT PRIMARY KEY,
        event_type TEXT NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
      );

      ALTER TABLE partnership_referrals 
      ADD COLUMN IF NOT EXISTS stripe_session_id TEXT UNIQUE;
    `);
  } catch (err) {
    console.warn('[BILLING DB INIT]', err.message);
  }
}
initBillingTables();

// Legacy hardcoded coupon codes (fallback if not found in DB)
const LEGACY_COUPONS = {
  // All 100% waiver passes strictly require administrative credentials (isAdmin: true)
  // No public zero-dollar bypass codes permitted
  'TEXASVIP': { discountPercent: 100, isAdmin: true, label: 'ADMIN FULL ACCESS (100% OFF)' },
  'TDLRADMIN': { discountPercent: 100, isAdmin: true, label: 'ADMIN COMPLIANCE PASS (100% OFF)' },
};

// Look up coupon from DB first, then fall back to legacy hardcoded codes
async function lookupCoupon(code) {
  const cleanCode = code.trim().toUpperCase();
  try {
    const result = await db.query(
      `SELECT c.*, p.partner_name, p.commission_percent AS partner_commission
       FROM coupons c
       LEFT JOIN partnerships p ON p.id = c.partnership_id
       WHERE c.code = $1`,
      [cleanCode]
    );
    if (result.rows.length > 0) {
      const c = result.rows[0];
      // Check if active and not expired and under max uses
      if (!c.is_active) return null;
      if (c.expires_at && new Date(c.expires_at) < new Date()) return null;
      if (c.max_uses && c.current_uses >= c.max_uses) return null;

      return {
        id: c.id,
        code: c.code,
        type: c.type,
        partnershipId: c.partnership_id,
        partnerName: c.partner_name,
        partnerCommission: c.partner_commission ? parseFloat(c.partner_commission) : null,
        discountType: c.discount_type,
        discountValue: parseFloat(c.discount_value) || 0,
        isAdmin: false,
        isPartner: c.type === 'PARTNER',
        label: c.type === 'PARTNER'
          ? `Partner: ${c.partner_name || 'Driving School'}`
          : `PROMO: ${c.code}`,
        // Map to legacy-compatible fields
        discountPercent: c.discount_type === 'PERCENT' ? parseFloat(c.discount_value) : undefined,
        discountAmount: c.discount_type === 'FLAT_CENTS' ? parseFloat(c.discount_value) : undefined,
        dbCoupon: true,
      };
    }
  } catch (err) {
    console.warn('[COUPON DB LOOKUP]', err.message);
  }
  // Fall back to legacy hardcoded codes
  const legacy = LEGACY_COUPONS[cleanCode];
  if (legacy) return { ...legacy, code: cleanCode, dbCoupon: false };
  return null;
}

// GET /api/v1/billing/pricing
// Public endpoint for landing page, checkout, and partner pricing displays
router.get('/pricing', async (req, res) => {
  try {
    const pricing = await getPricing();
    return res.json({ success: true, ...pricing });
  } catch (err) {
    return res.status(500).json({ success: false, error: err.message });
  }
});

// POST /api/v1/billing/validate-coupon
router.post('/validate-coupon', async (req, res) => {
  try {
    const { code = '' } = req.body;
    const cleanCode = code.trim().toUpperCase();
    const coupon = await lookupCoupon(cleanCode);

    if (!coupon) {
      return res.status(400).json({ success: false, valid: false, message: 'Invalid promo code.' });
    }

    const pricing = await getPricing();
    const baseAmount = pricing.coursePriceCents;
    let finalAmount = baseAmount;
    if (coupon.discountPercent === 100) {
      finalAmount = 0;
    } else if (coupon.discountPercent) {
      finalAmount = Math.round(baseAmount * (1 - coupon.discountPercent / 100));
    } else if (coupon.discountAmount) {
      finalAmount = Math.max(baseAmount - coupon.discountAmount, 0);
    }

    // Note: Do NOT increment coupon uses on validation.
    // Usage is strictly incremented upon verified checkout completion or waiver activation.

    // Check if user is logged in
    let userId = null;
    let token = req.cookies?.tx_session;
    if (!token && req.headers.authorization?.startsWith('Bearer ')) {
      token = req.headers.authorization.split(' ')[1];
    }
    if (token) {
      try {
        const payload = verifySessionJwt(token);
        userId = payload.id;
      } catch (e) {}
    }

    // If Admin legacy bypass code entered, restrict strictly to authorized admins with ADMIN_SECRET
    if (coupon.isAdmin) {
      const adminSecret = req.headers['x-admin-secret'] || req.body?.adminSecret;
      const isAuthorizedAdmin = (adminSecret && adminSecret === process.env.ADMIN_SECRET);

      if (!isAuthorizedAdmin) {
        return res.status(403).json({
          success: false,
          valid: false,
          message: 'This administrative bypass code requires state authorization.'
        });
      }
    }

    if (coupon.discountPercent === 100 || finalAmount === 0) {
      if (userId) {
        const freeSessionId = `free_${cleanCode.toLowerCase()}_${Date.now()}`;
        await db.query(
          `INSERT INTO enrollments (user_id, stripe_session_id, tier, amount_cents, status, paid_at, expires_at)
           VALUES ($1, $2, 'STANDARD', 0, 'ACTIVE', NOW(), NOW() + INTERVAL '90 days')
           ON CONFLICT (stripe_session_id) DO NOTHING`,
          [userId, freeSessionId]
        );
        await db.query(`UPDATE users SET enrollment_status = 'ACTIVE', updated_at = NOW() WHERE id = $1`, [userId]);
        await db.query(
          `INSERT INTO topic_progress (user_id, topic_id, module_id, status, unlocked_at)
           VALUES ($1, 'L01-T01', 1, 'UNLOCKED', NOW())
           ON CONFLICT (user_id, topic_id) DO UPDATE
           SET status = CASE WHEN topic_progress.status = 'COMPLETED' THEN 'COMPLETED' ELSE 'UNLOCKED' END`,
          [userId]
        );

        // Fetch user email for receipt
        const userRes = await db.query('SELECT email, full_name FROM users WHERE id = $1', [userId]);
        const userEmail = userRes.rows[0]?.email;
        const studentName = userRes.rows[0]?.full_name || 'Student';

        // Record in financial audit ledger
        await db.query(
          `INSERT INTO payment_transactions (
             user_id, stripe_session_id, tier,
             gross_amount_cents, discount_amount_cents, net_amount_cents,
             currency, coupon_code, status,
             customer_email, customer_name, payment_method_type,
             created_at, updated_at
           ) VALUES ($1, $2, 'STANDARD', 0, $3, 0, 'usd', $4, 'SUCCEEDED', $5, $6, 'promo_waiver', NOW(), NOW())
           ON CONFLICT (stripe_session_id) DO NOTHING`,
          [userId, freeSessionId, baseAmount, cleanCode, userEmail || 'student@texasade.org', studentName]
        ).catch((err) => console.warn('[LEDGER NOTICE]', err.message));

        // Increment coupon usage atomically on successful waiver activation
        if (coupon.dbCoupon && coupon.id) {
          db.query(`UPDATE coupons SET current_uses = current_uses + 1 WHERE id = $1`, [coupon.id]).catch(() => {});
        }

        // Send 100% tuition waiver enrollment confirmation receipt via Resend
        if (userEmail) {
          sendPaymentSuccessEmail({
            email: userEmail,
            fullName: studentName,
            amountCents: 0,
            sessionId: freeSessionId,
            tier: 'STANDARD',
            couponCode: cleanCode,
          }).catch((e) => console.warn('[EMAIL] Free waiver confirmation email dispatch error:', e.message));
        }

        return res.json({
          success: true,
          valid: true,
          label: coupon.label,
          discountPercent: 100,
          basePriceCents: baseAmount,
          finalPriceCents: 0,
          finalPriceFormatted: '$0.00',
          autoEnrolled: true,
          message: '100% Tuition Waiver Applied! Course unlocked.',
          redirectUrl: 'player.html',
        });
      } else {
        return res.json({
          success: true,
          valid: true,
          label: coupon.label,
          discountPercent: 100,
          basePriceCents: baseAmount,
          finalPriceCents: 0,
          finalPriceFormatted: '$0.00',
          autoEnrolled: false,
          message: '100% Tuition Waiver Applied. Course is completely free! Please sign in with Google to activate your access.',
        });
      }
    }

    return res.json({
      success: true,
      valid: true,
      isAdmin: false,
      isPartner: coupon.isPartner || false,
      partnerName: coupon.partnerName || null,
      label: coupon.label,
      discountPercent: coupon.discountPercent,
      discountAmount: coupon.discountAmount,
      finalPriceCents: finalAmount,
      finalPriceFormatted: `$${(finalAmount / 100).toFixed(2)}`,
      message: coupon.isPartner && finalAmount === baseAmount
        ? `Referral code from ${coupon.partnerName || 'partner'} applied!`
        : undefined,
    });
  } catch (err) {
    return res.status(500).json({ success: false, error: err.message });
  }
});

// POST /api/v1/billing/redeem-coupon
// Authenticated 100% coupon activator (Requires ADMIN_SECRET)
router.post('/redeem-coupon', requireAuth, async (req, res) => {
  try {
    const { code = '' } = req.body;
    const cleanCode = code.trim().toUpperCase();
    const coupon = await lookupCoupon(cleanCode);

    if (!coupon) {
      return res.status(400).json({ success: false, valid: false, message: 'Invalid promo code.' });
    }

    const userId = req.user.id;
    if (coupon.discountPercent === 100 || coupon.isAdmin) {
      const adminSecret = req.headers['x-admin-secret'] || req.body?.adminSecret;
      const isAuthorizedAdmin = (adminSecret && adminSecret === process.env.ADMIN_SECRET);

      if (!isAuthorizedAdmin) {
        return res.status(403).json({
          success: false,
          valid: false,
          message: 'This 100% waiver code requires administrative authorization.'
        });
      }

      const simSessionId = `admin_${cleanCode.toLowerCase()}_${Date.now()}`;
      await db.query(
        `INSERT INTO enrollments (user_id, stripe_session_id, tier, amount_cents, status, paid_at, expires_at)
         VALUES ($1, $2, 'STANDARD', 0, 'ACTIVE', NOW(), NOW() + INTERVAL '90 days')
         ON CONFLICT (stripe_session_id) DO NOTHING`,
        [userId, simSessionId]
      );
      await db.query(`UPDATE users SET enrollment_status = 'ACTIVE', updated_at = NOW() WHERE id = $1`, [userId]);
      return res.json({
        success: true,
        valid: true,
        isEnrolled: true,
        enrollmentStatus: 'ACTIVE',
        message: 'Admin Pass Activated! All 9 modules unlocked.',
      });
    }

    return res.json({
      success: true,
      valid: true,
      isEnrolled: false,
      discountPercent: coupon.discountPercent,
      message: `${coupon.label} applied.`,
    });
  } catch (err) {
    return res.status(500).json({ success: false, error: err.message });
  }
});

// POST /api/v1/billing/create-checkout-session
router.post('/create-checkout-session', optionalAuth, async (req, res) => {
  try {
    const { tier = 'STANDARD', clientOrigin, couponCode = '', email = '', fullName = '' } = req.body;
    let userId = req.user?.id;
    let userEmail = req.user?.email;

    // If student did not send Bearer token but provided email, auto-link user record
    if (!userId) {
      const cleanEmail = (email || '').trim().toLowerCase();
      if (cleanEmail && cleanEmail.includes('@')) {
        const cleanName = (fullName || cleanEmail.split('@')[0]).trim();
        const userRes = await db.query(
          `INSERT INTO users (email, full_name, enrollment_status)
           VALUES ($1, $2, 'UNPAID')
           ON CONFLICT (email) DO UPDATE SET full_name = COALESCE(EXCLUDED.full_name, users.full_name)
           RETURNING id, email`,
          [cleanEmail, cleanName]
        );
        userId = userRes.rows[0].id;
        userEmail = userRes.rows[0].email;
      }
    }

    if (!userId || !userEmail) {
      return res.status(401).json({
        success: false,
        error: 'AUTH_REQUIRED',
        message: 'Please sign in with Google or provide your student email so your state certification is registered.'
      });
    }

    const cleanCoupon = couponCode.trim().toUpperCase();
    const returnBase = clientOrigin || process.env.CLIENT_URL || 'http://localhost:8080';

    // Handle Admin inspection bypass codes (Requires ADMIN_SECRET)
    if (['TEXASVIP', 'TDLRADMIN'].includes(cleanCoupon)) {
      const adminSecret = req.headers['x-admin-secret'] || req.body?.adminSecret;
      const isAuthorizedAdmin = (adminSecret && adminSecret === process.env.ADMIN_SECRET);
      if (!isAuthorizedAdmin) {
        return res.status(403).json({
          success: false,
          message: 'Administrative bypass codes cannot be redeemed without state authorization.'
        });
      }
      const simSessionId = `admin_${cleanCoupon.toLowerCase()}_${Date.now()}`;
      await db.query(
        `INSERT INTO enrollments (user_id, stripe_session_id, tier, amount_cents, status, paid_at, expires_at)
         VALUES ($1, $2, $3, 0, 'ACTIVE', NOW(), NOW() + INTERVAL '90 days')
         ON CONFLICT (stripe_session_id) DO NOTHING`,
        [userId, simSessionId, tier]
      );
      await db.query(`UPDATE users SET enrollment_status = 'ACTIVE', updated_at = NOW() WHERE id = $1`, [userId]);
      await db.query(
        `INSERT INTO topic_progress (user_id, topic_id, module_id, status, unlocked_at)
         VALUES ($1, 'L01-T01', 1, 'UNLOCKED', NOW())
         ON CONFLICT (user_id, topic_id) DO UPDATE
         SET status = CASE WHEN topic_progress.status = 'COMPLETED' THEN 'COMPLETED' ELSE 'UNLOCKED' END`,
        [userId]
      );
      return res.json({
        success: true,
        adminBypass: true,
        checkoutUrl: `${returnBase}/player.html`,
      });
    }

    const pricing = await getPricing();
    const defaultCourseCents = pricing.coursePriceCents;
    const defaultRushCents = pricing.rushPriceCents;
    const totalExpressCents = defaultCourseCents + defaultRushCents;

    if (!hasRealStripeKey) {
      if (process.env.NODE_ENV === 'production') {
        return res.status(503).json({
          success: false,
          error: 'PAYMENT_GATEWAY_NOT_CONFIGURED',
          message: 'Payment gateway configuration pending. Please contact support@texasade.org.'
        });
      }
      // Development mode: activate enrollment immediately
      const simSessionId = `sim_${Date.now()}`;
      await db.query(
        `INSERT INTO enrollments (user_id, stripe_session_id, tier, amount_cents, status, paid_at, expires_at)
         VALUES ($1, $2, $3, $4, 'ACTIVE', NOW(), NOW() + INTERVAL '90 days')
         ON CONFLICT (stripe_session_id) DO NOTHING`,
        [userId, simSessionId, tier, tier === 'EXPRESS' ? totalExpressCents : defaultCourseCents]
      );
      await db.query(`UPDATE users SET enrollment_status = 'ACTIVE', updated_at = NOW() WHERE id = $1`, [userId]);
      await db.query(
        `INSERT INTO topic_progress (user_id, topic_id, module_id, status, unlocked_at)
         VALUES ($1, 'L01-T01', 1, 'UNLOCKED', NOW())
         ON CONFLICT (user_id, topic_id) DO UPDATE
         SET status = CASE WHEN topic_progress.status = 'COMPLETED' THEN 'COMPLETED' ELSE 'UNLOCKED' END`,
        [userId]
      );
      return res.json({
        success: true,
        simulated: true,
        checkoutUrl: `${returnBase}/checkout.html?status=success&simulated=true`,
      });
    }

    let coursePriceCents = defaultCourseCents;
    const coupon = cleanCoupon ? await lookupCoupon(cleanCoupon) : null;
    if (coupon && !coupon.isAdmin) {
      if (coupon.discountPercent === 100) {
        coursePriceCents = 0;
      } else if (coupon.discountPercent) {
        coursePriceCents = Math.round(coursePriceCents * (1 - coupon.discountPercent / 100));
      } else if (coupon.discountAmount) {
        coursePriceCents = Math.max(coursePriceCents - coupon.discountAmount, 0);
      }
    }

    if (tier === 'STANDARD' && coursePriceCents === 0) {
      // Security Check: 100% fee waivers require verified administrative secret
      const adminSecret = req.headers['x-admin-secret'] || req.body?.adminSecret;
      const isAuthorizedAdmin = (adminSecret && adminSecret === process.env.ADMIN_SECRET);
      if (!isAuthorizedAdmin) {
        return res.status(403).json({
          success: false,
          error: 'UNAUTHORIZED_WAIVER',
          message: '100% promotional fee waivers require authorized administrative verification.'
        });
      }

      // 100% free enrollment via verified administrative waiver
      const freeSessionId = `free_${(cleanCoupon || 'promo').toLowerCase()}_${Date.now()}`;
      await db.query(
        `INSERT INTO enrollments (user_id, stripe_session_id, tier, amount_cents, status, paid_at, expires_at)
         VALUES ($1, $2, $3, 0, 'ACTIVE', NOW(), NOW() + INTERVAL '90 days')
         ON CONFLICT (stripe_session_id) DO NOTHING`,
        [userId, freeSessionId, tier]
      );
      await db.query(`UPDATE users SET enrollment_status = 'ACTIVE', updated_at = NOW() WHERE id = $1`, [userId]);
      await db.query(
        `INSERT INTO topic_progress (user_id, topic_id, module_id, status, unlocked_at)
         VALUES ($1, 'L01-T01', 1, 'UNLOCKED', NOW())
         ON CONFLICT (user_id, topic_id) DO UPDATE
         SET status = CASE WHEN topic_progress.status = 'COMPLETED' THEN 'COMPLETED' ELSE 'UNLOCKED' END`,
        [userId]
      );

      // Record in financial audit ledger
      await db.query(
        `INSERT INTO payment_transactions (
           user_id, stripe_session_id, tier,
           gross_amount_cents, discount_amount_cents, net_amount_cents,
           currency, coupon_code, status,
           customer_email, customer_name, payment_method_type,
           created_at, updated_at
         ) VALUES ($1, $2, $3, 0, $4, 0, 'usd', $5, 'SUCCEEDED', $6, $7, 'promo_waiver', NOW(), NOW())
         ON CONFLICT (stripe_session_id) DO NOTHING`,
        [userId, freeSessionId, tier, defaultCourseCents, cleanCoupon, userEmail, fullName || userEmail.split('@')[0]]
      ).catch((err) => console.warn('[LEDGER NOTICE]', err.message));

      if (coupon && coupon.dbCoupon && coupon.id) {
        db.query(`UPDATE coupons SET current_uses = current_uses + 1 WHERE id = $1`, [coupon.id]).catch(() => {});
      }

      // Send 100% waiver confirmation email
      if (userEmail) {
        sendPaymentSuccessEmail({
          email: userEmail,
          fullName: fullName || userEmail.split('@')[0],
          amountCents: 0,
          sessionId: freeSessionId,
          tier,
          couponCode: cleanCoupon,
        }).catch((e) => console.warn('[EMAIL] Free waiver confirmation email dispatch error:', e.message));
      }

      return res.json({
        success: true,
        freeEnrollment: true,
        checkoutUrl: `${returnBase}/player.html`,
      });
    }

    const lineItems = [
      {
        price_data: {
          currency: 'usd',
          product_data: {
            name: coupon && !coupon.isAdmin
              ? `Texas Adult Driver Education (ADE-1317) - ${coupon.label}`
              : 'Texas Adult Driver Education (6-Hour TDLR Course)',
            description: 'TDLR Approved Course ADE-1317. Mandatory 6-hour certification for drivers aged 18-24 (valid for all adults 18+).',
          },
          unit_amount: coursePriceCents,
        },
        quantity: 1,
      },
    ];

    if (tier === 'EXPRESS') {
      lineItems.push({
        price_data: {
          currency: 'usd',
          product_data: {
            name: 'Same-Day Express Certificate Delivery',
            description: 'Priority processing and same-day electronic certificate generation upon course completion.',
          },
          unit_amount: defaultRushCents,
        },
        quantity: 1,
      });
    }

    const sessionOptions = (rawStripeKey.startsWith('oak_') || stripeAccountId)
      ? { stripeAccount: stripeAccountId }
      : undefined;

    let session;
    try {
      session = await stripe.checkout.sessions.create({
        payment_method_types: ['card'],
        mode: 'payment',
        customer_email: userEmail,
        client_reference_id: userId,
        line_items: lineItems,
        metadata: {
          userId,
          tier,
          couponCode: cleanCoupon || '',
        },
        success_url: `${returnBase}/checkout.html?status=success&session_id={CHECKOUT_SESSION_ID}`,
        cancel_url: `${returnBase}/checkout.html?status=cancelled`,
      }, sessionOptions);
    } catch (stripeErr) {
      console.error('[STRIPE CHECKOUT ERROR]', stripeErr.message);
      return res.status(503).json({
        success: false,
        error: 'PAYMENT_GATEWAY_UNAVAILABLE',
        message: 'The secure credit card gateway is currently updating. Please try again in a few moments or contact support@texasade.org.'
      });
    }

    const finalAmountCents = tier === 'EXPRESS' ? (coursePriceCents + defaultRushCents) : coursePriceCents;
    const discountCents = defaultCourseCents - coursePriceCents;

    // Record pending enrollment and pending audit transaction
    try {
      await db.query(
        `INSERT INTO enrollments (user_id, stripe_session_id, tier, amount_cents, status)
         VALUES ($1, $2, $3, $4, 'PENDING_PAYMENT')
         ON CONFLICT (stripe_session_id) DO NOTHING`,
        [userId, session.id, tier, finalAmountCents]
      );
      await db.query(
        `INSERT INTO payment_transactions (
           user_id, stripe_session_id, tier,
           gross_amount_cents, discount_amount_cents, rush_amount_cents,
           net_amount_cents, currency, coupon_code, status,
           customer_email, customer_name, payment_method_type,
           created_at, updated_at
         ) VALUES ($1, $2, $3, $4, $5, $6, $7, 'usd', $8, 'PENDING', $9, $10, 'card', NOW(), NOW())
         ON CONFLICT (stripe_session_id) DO NOTHING`,
        [
          userId, session.id, tier,
          finalAmountCents, discountCents, (tier === 'EXPRESS' ? defaultRushCents : 0),
          finalAmountCents, cleanCoupon || null, userEmail, (fullName || userEmail.split('@')[0])
        ]
      );
    } catch (dbErr) {
      console.warn('[BILLING DB] Pending enrollment non-blocking log:', dbErr.message);
    }

    return res.json({ success: true, checkoutUrl: session.url, sessionId: session.id });
  } catch (err) {
    console.error('[STRIPE ERROR]', err);
    return res.status(500).json({ success: false, error: err.message });
  }
});

// POST /api/v1/billing/webhook
router.post('/webhook', express.raw({ type: 'application/json' }), async (req, res) => {
  const sig = req.headers['stripe-signature'];
  const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET;

  let event;
  try {
    if (webhookSecret && webhookSecret !== 'PLACEHOLDER') {
      event = stripe.webhooks.constructEvent(req.body, sig, webhookSecret);
    } else {
      if (process.env.NODE_ENV === 'production') {
        console.error('[STRIPE WEBHOOK] Missing webhook secret in production.');
        return res.status(400).send('Webhook Secret Not Configured');
      }
      // Dev mode fallback
      event = JSON.parse(req.body.toString('utf-8'));
    }
  } catch (err) {
    console.error('[WEBHOOK ERROR] Signature verification failed:', err.message);
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  // Strict Event Deduplication & Idempotency Check
  const eventId = event.id;
  if (eventId) {
    try {
      const existing = await db.query('SELECT event_id FROM processed_stripe_events WHERE event_id = $1', [eventId]);
      if (existing.rows.length > 0) {
        console.log(`[STRIPE WEBHOOK] Idempotent duplicate event bypassed: ${eventId}`);
        return res.json({ received: true, duplicate: true });
      }
      await db.query(
        'INSERT INTO processed_stripe_events (event_id, event_type, created_at) VALUES ($1, $2, NOW()) ON CONFLICT (event_id) DO NOTHING',
        [eventId, event.type]
      );
    } catch (idempErr) {
      console.warn('[WEBHOOK IDEMPOTENCY CHECK]', idempErr.message);
    }
  }

  // 1. PAYMENT COMPLETED & ENROLLMENT ACTIVATION
  if (event.type === 'checkout.session.completed') {
    const session = event.data.object;
    const userId = session.client_reference_id || session.metadata?.userId;
    const tier = session.metadata?.tier || 'STANDARD';
    const livePricing = await getPricing();
    const amountCents = (session.amount_total !== undefined && session.amount_total !== null)
      ? session.amount_total
      : livePricing.coursePriceCents;

    console.log(`[STRIPE WEBHOOK] Payment successful for user ${userId}, session ${session.id}, amount: $${(amountCents / 100).toFixed(2)}`);

    try {
      // 1. Update or insert enrollment record
      await db.query(
        `INSERT INTO enrollments (user_id, stripe_session_id, stripe_payment_intent, tier, amount_cents, status, paid_at, expires_at)
         VALUES ($1, $2, $3, $4, $5, 'ACTIVE', NOW(), NOW() + INTERVAL '90 days')
         ON CONFLICT (stripe_session_id) DO UPDATE
         SET status = 'ACTIVE',
             stripe_payment_intent = EXCLUDED.stripe_payment_intent,
             paid_at = NOW(),
             expires_at = NOW() + INTERVAL '90 days'`,
        [userId, session.id, session.payment_intent, tier, amountCents]
      );

      // 2. Set user enrollment_status = 'ACTIVE'
      await db.query(
        `UPDATE users SET enrollment_status = 'ACTIVE', updated_at = NOW() WHERE id = $1`,
        [userId]
      );

      // 3. Unlock Topic L01-T01
      await db.query(
        `INSERT INTO topic_progress (user_id, topic_id, module_id, status, unlocked_at)
         VALUES ($1, 'L01-T01', 1, 'UNLOCKED', NOW())
         ON CONFLICT (user_id, topic_id) DO UPDATE
         SET status = CASE WHEN topic_progress.status = 'COMPLETED' THEN 'COMPLETED' ELSE 'UNLOCKED' END`,
        [userId]
      );

      // 4. Initialize module 1 progress as IN_PROGRESS
      await db.query(
        `INSERT INTO module_progress (user_id, module_id, status)
         VALUES ($1, 1, 'IN_PROGRESS')
         ON CONFLICT (user_id, module_id) DO NOTHING`,
        [userId]
      );

      // 5. Calculate processing fee and record in immutable financial audit ledger
      const stripeFeeCents = Math.round(amountCents * 0.029 + 30);
      const netAmountCents = Math.max(0, amountCents - stripeFeeCents);
      const webhookCouponCode = (session.metadata?.couponCode || '').trim().toUpperCase();

      const userRes = await db.query('SELECT email, full_name FROM users WHERE id = $1', [userId]);
      const studentEmail = userRes.rows[0]?.email || session.customer_details?.email || session.customer_email || 'student@texasade.org';
      const studentName = userRes.rows[0]?.full_name || session.customer_details?.name || 'Student';

      await db.query(
        `INSERT INTO payment_transactions (
           user_id, stripe_session_id, stripe_payment_intent, tier,
           gross_amount_cents, discount_amount_cents, rush_amount_cents,
           stripe_fee_cents, net_amount_cents, currency,
           coupon_code, status, customer_email, customer_name,
           payment_method_type, created_at, updated_at
         ) VALUES ($1, $2, $3, $4, $5, 0, $6, $7, $8, $9, $10, 'SUCCEEDED', $11, $12, 'card', NOW(), NOW())
         ON CONFLICT (stripe_session_id) DO UPDATE SET
           stripe_payment_intent = EXCLUDED.stripe_payment_intent,
           status = 'SUCCEEDED',
           gross_amount_cents = EXCLUDED.gross_amount_cents,
           stripe_fee_cents = EXCLUDED.stripe_fee_cents,
           net_amount_cents = EXCLUDED.net_amount_cents,
           updated_at = NOW()`,
        [
          userId, session.id, session.payment_intent, tier,
          amountCents, (tier === 'EXPRESS' ? livePricing.rushPriceCents : 0),
          stripeFeeCents, netAmountCents, session.currency || 'usd',
          webhookCouponCode || null, studentEmail, studentName
        ]
      ).catch((err) => console.warn('[LEDGER SUCCEEDED NOTICE]', err.message));

      // 6. Increment coupon usage counter on completed checkout
      if (webhookCouponCode) {
        db.query('UPDATE coupons SET current_uses = current_uses + 1, updated_at = NOW() WHERE code = $1', [webhookCouponCode]).catch(() => {});
      }

      console.log(`[STRIPE WEBHOOK] User ${userId} activated and L01-T01 unlocked successfully.`);

      // 7. Dispatch clean branded payment receipt via Resend
      if (studentEmail) {
        sendPaymentSuccessEmail({
          email: studentEmail,
          fullName: studentName,
          amountCents,
          sessionId: session.id,
          tier,
          couponCode: webhookCouponCode || null,
        }).catch((e) => console.warn('[EMAIL] Payment success email dispatch error:', e.message));
      }

      // 8. PARTNER REFERRAL TRACKING — Credit partner commission with strict idempotency
      if (webhookCouponCode) {
        try {
          const couponRes = await db.query(
            `SELECT c.id, c.type, c.partnership_id, p.commission_percent
             FROM coupons c
             LEFT JOIN partnerships p ON p.id = c.partnership_id
             WHERE c.code = $1 AND c.type = 'PARTNER' AND c.partnership_id IS NOT NULL`,
            [webhookCouponCode]
          );
          if (couponRes.rows.length > 0) {
            const cp = couponRes.rows[0];
            const commPercent = parseFloat(cp.commission_percent) || 10;
            const commissionCents = Math.round(amountCents * (commPercent / 100));

            // Record the referral with unique stripe_session_id (guarantees zero duplicate rows on retries)
            const refInsert = await db.query(
              `INSERT INTO partnership_referrals (partnership_id, user_id, referral_code, amount_cents, commission_cents, status, stripe_session_id)
               VALUES ($1, $2, $3, $4, $5, 'CREDITED', $6)
               ON CONFLICT (stripe_session_id) DO NOTHING
               RETURNING id`,
              [cp.partnership_id, userId, webhookCouponCode, amountCents, commissionCents, session.id]
            );

            // Update partnership aggregates ONLY if referral was newly inserted
            if (refInsert.rows.length > 0) {
              await db.query(
                `UPDATE partnerships
                 SET total_referrals = total_referrals + 1,
                     total_conversions = total_conversions + 1,
                     total_revenue_cents = total_revenue_cents + $1,
                     total_commission_cents = total_commission_cents + $2,
                     updated_at = NOW()
                 WHERE id = $3`,
                [amountCents, commissionCents, cp.partnership_id]
              );
              console.log(`[WEBHOOK REFERRAL] Partner ${cp.partnership_id} credited ${commissionCents} cents (${commPercent}% of ${amountCents})`);
            }
          }
        } catch (refErr) {
          console.warn('[WEBHOOK REFERRAL ERROR]', refErr.message);
        }
      }
    } catch (dbErr) {
      console.error('[STRIPE WEBHOOK DB ERROR]', dbErr);
      return res.status(500).json({ error: 'Database update failed' });
    }
  }

  // 2. PAYMENT FAILED ALERT
  if (event.type === 'payment_intent.payment_failed') {
    const intent = event.data.object;
    const errorMsg = intent.last_payment_error?.message || 'Payment method declined';
    const customerEmail = intent.receipt_email || intent.customer_details?.email;
    const customerName = intent.customer_details?.name || 'Student';

    console.warn(`[STRIPE WEBHOOK] Payment failed for ${customerEmail}: ${errorMsg}`);

    // Update financial audit ledger
    if (intent.id) {
      db.query(`UPDATE payment_transactions SET status = 'FAILED', updated_at = NOW() WHERE stripe_payment_intent = $1`, [intent.id]).catch(() => {});
    }

    if (customerEmail) {
      sendPaymentFailedEmail({
        email: customerEmail,
        fullName: customerName,
        reason: errorMsg,
      }).catch((e) => console.warn('[EMAIL] Payment failed email dispatch error:', e.message));
    }
  }

  // 3. CHARGE REFUNDED (REVOKE ENROLLMENT & UPDATE ACCOUNTING LEDGER PER TDLR COMPLIANCE)
  if (event.type === 'charge.refunded') {
    const charge = event.data.object;
    const paymentIntentId = charge.payment_intent;
    const refundAmountCents = charge.amount_refunded || 0;

    if (paymentIntentId) {
      try {
        await db.query(
          `UPDATE payment_transactions
           SET status = 'REFUNDED',
               refund_amount_cents = $1,
               refunded_at = NOW(),
               updated_at = NOW()
           WHERE stripe_payment_intent = $2`,
          [refundAmountCents, paymentIntentId]
        );
        await db.query(`UPDATE enrollments SET status = 'REFUNDED' WHERE stripe_payment_intent = $1`, [paymentIntentId]);
        await db.query(
          `UPDATE users SET enrollment_status = 'REFUNDED', updated_at = NOW()
           WHERE id IN (SELECT user_id FROM enrollments WHERE stripe_payment_intent = $1)`,
          [paymentIntentId]
        );
        console.log(`[STRIPE WEBHOOK] Enrollment revoked and refund recorded for payment intent: ${paymentIntentId} ($${(refundAmountCents/100).toFixed(2)})`);
      } catch (refundErr) {
        console.error('[STRIPE WEBHOOK REFUND ERROR]', refundErr);
      }
    }
  }

  return res.json({ received: true });
});

module.exports = router;
