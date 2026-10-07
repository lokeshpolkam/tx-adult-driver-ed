const express = require('express');
const router = express.Router();
const Stripe = require('stripe');
const db = require('../db');
const { requireAuth, verifySessionJwt } = require('../auth');

const rawStripeKey = (process.env.STRIPE_SECRET_KEY || 'PLACEHOLDER').trim();
const hasRealStripeKey = rawStripeKey.startsWith('sk_') && rawStripeKey !== 'sk_test_placeholder';
const stripe = hasRealStripeKey ? new Stripe(rawStripeKey) : null;

// Coupon codes configuration
const COUPONS = {
  'TEXAS100': { discountPercent: 100, isAdmin: true, label: '100% OFF FULL COURSE ACCESS' },
  'FREE100': { discountPercent: 100, isAdmin: true, label: '100% OFF COMPLIMENTARY ACCESS' },
  'TEXASVIP': { discountPercent: 100, isAdmin: true, label: 'ADMIN FULL ACCESS (100% OFF)' },
  'TDLRADMIN': { discountPercent: 100, isAdmin: true, label: 'ADMIN COMPLIANCE PASS (100% OFF)' },
  'DRIVETEXAS': { discountPercent: 50, isAdmin: false, label: '50% SPECIAL SAVINGS' },
  'LONE10': { discountAmount: 1000, isAdmin: false, label: '$10 STATE DISCOUNT' },
};

// POST /api/v1/billing/validate-coupon
router.post('/validate-coupon', async (req, res) => {
  try {
    const { code = '' } = req.body;
    const cleanCode = code.trim().toUpperCase();
    const coupon = COUPONS[cleanCode];

    if (!coupon) {
      return res.status(400).json({ success: false, valid: false, message: 'Invalid promo code.' });
    }

    const baseAmount = 3800; // $38.00
    let finalAmount = baseAmount;
    if (coupon.discountPercent === 100) {
      finalAmount = 0;
    } else if (coupon.discountPercent) {
      finalAmount = Math.round(baseAmount * (1 - coupon.discountPercent / 100));
    } else if (coupon.discountAmount) {
      finalAmount = Math.max(baseAmount - coupon.discountAmount, 0);
    }

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

    // If Admin 100% coupon entered, directly activate student in Cloud SQL!
    if (coupon.isAdmin) {
      if (userId) {
        const simSessionId = `admin_${cleanCode.toLowerCase()}_${Date.now()}`;
        await db.query(
          `INSERT INTO enrollments (user_id, stripe_session_id, tier, amount_cents, status, paid_at, expires_at)
           VALUES ($1, $2, 'STANDARD', 0, 'ACTIVE', NOW(), NOW() + INTERVAL '90 days')
           ON CONFLICT (stripe_session_id) DO NOTHING`,
          [userId, simSessionId]
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
          valid: true,
          isAdmin: true,
          label: coupon.label,
          finalPriceCents: 0,
          finalPriceFormatted: '$0.00',
          autoEnrolled: true,
          message: 'Admin VIP Pass Activated! Course unlocked with full access.',
          redirectUrl: 'player.html?access=admin_vip_granted',
        });
      } else {
        return res.json({
          success: true,
          valid: true,
          isAdmin: true,
          label: coupon.label,
          finalPriceCents: 0,
          finalPriceFormatted: '$0.00',
          autoEnrolled: false,
          requiresAuth: true,
          message: 'Admin VIP Pass verified (100% OFF)! Sign in with Google above to activate your access.',
        });
      }
    }

    return res.json({
      success: true,
      valid: true,
      isAdmin: false,
      label: coupon.label,
      finalPriceCents: finalAmount,
      finalPriceFormatted: `$${(finalAmount / 100).toFixed(2)}`,
    });
  } catch (err) {
    return res.status(500).json({ success: false, error: err.message });
  }
});

// POST /api/v1/billing/create-checkout-session
router.post('/create-checkout-session', requireAuth, async (req, res) => {
  try {
    const { tier = 'STANDARD', clientOrigin, couponCode = '' } = req.body;
    const userId = req.user.id;
    const userEmail = req.user.email;
    const cleanCoupon = couponCode.trim().toUpperCase();

    const returnBase = clientOrigin || process.env.CLIENT_URL || 'http://localhost:8080';

    // Handle Admin bypass coupon
    if (cleanCoupon === 'TEXASVIP' || cleanCoupon === 'TDLRADMIN') {
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
        checkoutUrl: `${returnBase}/index.html?access=admin_vip_granted`,
      });
    }

    if (!hasRealStripeKey) {
      // Development mode: activate enrollment immediately
      const simSessionId = `sim_${Date.now()}`;
      await db.query(
        `INSERT INTO enrollments (user_id, stripe_session_id, tier, amount_cents, status, paid_at, expires_at)
         VALUES ($1, $2, $3, $4, 'ACTIVE', NOW(), NOW() + INTERVAL '90 days')
         ON CONFLICT (stripe_session_id) DO NOTHING`,
        [userId, simSessionId, tier, tier === 'EXPRESS' ? 4799 : 3800]
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
        checkoutUrl: `${returnBase}/index.html?payment=simulated_success`,
      });
    }

    const lineItems = [
      {
        price_data: {
          currency: 'usd',
          product_data: {
            name: 'Texas Adult Driver Education (6-Hour TDLR Course)',
            description: 'TDLR Approved Course ADE-1317. Mandatory 6-hour certification for drivers aged 18-24 (valid for all adults 18+).',
          },
          unit_amount: 3800, // $38.00
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
          unit_amount: 999, // $9.99
        },
        quantity: 1,
      });
    }

    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      mode: 'payment',
      customer_email: userEmail,
      client_reference_id: userId,
      line_items: lineItems,
      metadata: {
        userId,
        tier,
      },
      success_url: `${returnBase}/dashboard?payment=success&session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${returnBase}/checkout?payment=cancelled`,
    });

    // Record pending enrollment
    await db.query(
      `INSERT INTO enrollments (user_id, stripe_session_id, tier, amount_cents, status)
       VALUES ($1, $2, $3, $4, 'PENDING_PAYMENT')
       ON CONFLICT (stripe_session_id) DO NOTHING`,
      [userId, session.id, tier, tier === 'EXPRESS' ? 4799 : 3800]
    );

    return res.json({ success: true, checkoutUrl: session.url, sessionId: session.id });
  } catch (err) {
    console.error('[STRIPE ERROR]', err);
    return res.status(500).json({ success: false, error: err.message });
  }
});

// POST /api/v1/webhooks/stripe
router.post('/webhook', express.raw({ type: 'application/json' }), async (req, res) => {
  const sig = req.headers['stripe-signature'];
  const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET;

  let event;
  try {
    if (webhookSecret && webhookSecret !== 'PLACEHOLDER') {
      event = stripe.webhooks.constructEvent(req.body, sig, webhookSecret);
    } else {
      // In dev fallback, parse raw JSON
      event = JSON.parse(req.body.toString('utf-8'));
    }
  } catch (err) {
    console.error('[WEBHOOK ERROR] Signature verification failed:', err.message);
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  if (event.type === 'checkout.session.completed') {
    const session = event.data.object;
    const userId = session.client_reference_id || session.metadata?.userId;
    const tier = session.metadata?.tier || 'STANDARD';
    const amountCents = session.amount_total || 3800;

    console.log(`[STRIPE WEBHOOK] Payment successful for user ${userId}, session ${session.id}`);

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

      console.log(`[STRIPE WEBHOOK] User ${userId} activated and L01-T01 unlocked successfully.`);
    } catch (dbErr) {
      console.error('[STRIPE WEBHOOK DB ERROR]', dbErr);
      return res.status(500).json({ error: 'Database update failed' });
    }
  }

  return res.json({ received: true });
});

module.exports = router;
