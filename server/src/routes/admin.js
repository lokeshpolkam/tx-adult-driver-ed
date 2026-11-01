const express = require('express');
const router = express.Router();
const crypto = require('crypto');
const db = require('../db');
const { verifySessionJwt, verifyGoogleIdToken, mintSessionJwt } = require('../auth');
const { sendAdminInvitationEmail } = require('../email');
const { getPricing, invalidatePricingCache } = require('../pricing');

const PRIMARY_ADMIN_EMAIL = process.env.PRIMARY_ADMIN_EMAIL || 'admin@texasade.org';
const SUPER_ADMIN_EMAILS = [PRIMARY_ADMIN_EMAIL];

// Auto-initialize admin tables if needed
async function initAdminTables() {
  try {
    await db.query(`
      CREATE TABLE IF NOT EXISTS admin_invitations (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        invited_email TEXT NOT NULL,
        token_hash TEXT NOT NULL UNIQUE,
        invited_by UUID REFERENCES users(id) ON DELETE SET NULL,
        status TEXT NOT NULL DEFAULT 'PENDING',
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        expires_at TIMESTAMPTZ NOT NULL DEFAULT (NOW() + INTERVAL '24 hours'),
        accepted_at TIMESTAMPTZ,
        accepted_by UUID REFERENCES users(id) ON DELETE SET NULL
      );
      CREATE INDEX IF NOT EXISTS idx_admin_invitations_email ON admin_invitations(invited_email);
      CREATE INDEX IF NOT EXISTS idx_admin_invitations_token ON admin_invitations(token_hash);
      CREATE INDEX IF NOT EXISTS idx_admin_invitations_status ON admin_invitations(status);
      UPDATE users SET role = 'ADMIN' WHERE LOWER(email) = LOWER(PRIMARY_ADMIN_EMAIL);

      CREATE TABLE IF NOT EXISTS partnerships (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        partner_name TEXT NOT NULL,
        contact_name TEXT,
        contact_email TEXT NOT NULL,
        contact_phone TEXT,
        referral_code TEXT UNIQUE NOT NULL,
        commission_percent NUMERIC(5,2) NOT NULL DEFAULT 10.00,
        status TEXT NOT NULL DEFAULT 'ACTIVE',
        total_referrals INTEGER DEFAULT 0,
        total_conversions INTEGER DEFAULT 0,
        total_revenue_cents INTEGER DEFAULT 0,
        total_commission_cents INTEGER DEFAULT 0,
        total_paid_out_cents INTEGER DEFAULT 0,
        notes TEXT,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NOW(),
        created_by UUID REFERENCES users(id) ON DELETE SET NULL
      );
      CREATE INDEX IF NOT EXISTS idx_partnerships_code ON partnerships(referral_code);
      CREATE INDEX IF NOT EXISTS idx_partnerships_status ON partnerships(status);

      CREATE TABLE IF NOT EXISTS partnership_referrals (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        partnership_id UUID REFERENCES partnerships(id) ON DELETE CASCADE,
        user_id UUID REFERENCES users(id) ON DELETE SET NULL,
        referral_code TEXT NOT NULL,
        amount_cents INTEGER DEFAULT 0,
        commission_cents INTEGER DEFAULT 0,
        status TEXT DEFAULT 'PENDING',
        created_at TIMESTAMPTZ DEFAULT NOW()
      );
      CREATE INDEX IF NOT EXISTS idx_partnership_referrals_pid ON partnership_referrals(partnership_id);

      CREATE TABLE IF NOT EXISTS coupons (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        code TEXT UNIQUE NOT NULL,
        type TEXT NOT NULL DEFAULT 'PROMO',
        partnership_id UUID REFERENCES partnerships(id) ON DELETE CASCADE,
        discount_type TEXT NOT NULL DEFAULT 'NONE',
        discount_value NUMERIC(10,2) DEFAULT 0,
        max_uses INTEGER,
        current_uses INTEGER DEFAULT 0,
        is_active BOOLEAN DEFAULT true,
        expires_at TIMESTAMPTZ,
        created_by UUID REFERENCES users(id) ON DELETE SET NULL,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NOW()
      );
      CREATE INDEX IF NOT EXISTS idx_coupons_code ON coupons(code);

      CREATE TABLE IF NOT EXISTS withdrawal_requests (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        partnership_id UUID REFERENCES partnerships(id) ON DELETE CASCADE,
        amount_cents INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'PENDING',
        payment_method TEXT,
        payment_details TEXT,
        admin_notes TEXT,
        reviewed_by UUID REFERENCES users(id) ON DELETE SET NULL,
        reviewed_at TIMESTAMPTZ,
        paid_at TIMESTAMPTZ,
        created_at TIMESTAMPTZ DEFAULT NOW()
      );
      CREATE INDEX IF NOT EXISTS idx_withdrawal_requests_pid ON withdrawal_requests(partnership_id);
      CREATE INDEX IF NOT EXISTS idx_withdrawal_requests_status ON withdrawal_requests(status);

      CREATE TABLE IF NOT EXISTS partner_access_keys (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        partnership_id UUID REFERENCES partnerships(id) ON DELETE CASCADE,
        key_hash TEXT UNIQUE NOT NULL,
        is_active BOOLEAN DEFAULT true,
        created_at TIMESTAMPTZ DEFAULT NOW()
      );
      CREATE INDEX IF NOT EXISTS idx_partner_access_keys_hash ON partner_access_keys(key_hash);

      CREATE TABLE IF NOT EXISTS pricing_config (
        id VARCHAR(32) PRIMARY KEY DEFAULT 'default',
        course_price_cents INTEGER NOT NULL DEFAULT 3800,
        rush_certificate_price_cents INTEGER NOT NULL DEFAULT 999,
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_by UUID REFERENCES users(id) ON DELETE SET NULL
      );
      INSERT INTO pricing_config (id, course_price_cents, rush_certificate_price_cents)
      VALUES ('default', 3800, 999)
      ON CONFLICT (id) DO NOTHING;
    `);
  } catch (err) {
    console.warn('[ADMIN DB INIT]', err.message);
  }
}
initAdminTables();

// Stealth Require Admin Middleware
// Returns 404 instead of 403 to prevent revealing the existence of the admin endpoint
function requireAdmin(req, res, next) {
  let token = req.cookies?.tx_session;
  if (!token && req.headers.authorization?.startsWith('Bearer ')) {
    token = req.headers.authorization.split(' ')[1];
  }

  if (!token) {
    return res.status(404).json({ success: false, error: 'NOT_FOUND' });
  }

  try {
    const payload = verifySessionJwt(token);
    const userEmail = (payload.email || '').toLowerCase().trim();
    const isSuperAdmin = SUPER_ADMIN_EMAILS.includes(userEmail);
    if (payload.role === 'ADMIN' || isSuperAdmin) {
      req.user = payload;
      return next();
    }
    return res.status(404).json({ success: false, error: 'NOT_FOUND' });
  } catch (err) {
    console.warn('[REQUIRE_ADMIN REJECTED]', err.message);
    return res.status(404).json({ success: false, error: 'NOT_FOUND' });
  }
}

// ---------------------------------------------------------------------
// PUBLIC INVITATION ENDPOINTS (For Recipients)
// ---------------------------------------------------------------------

// GET /api/v1/admin/invitations/verify?token=...
router.get('/invitations/verify', async (req, res) => {
  try {
    const { token } = req.query;
    if (!token) {
      return res.status(400).json({ valid: false, reason: 'MISSING_TOKEN', message: 'Invitation token is missing.' });
    }

    const tokenHash = crypto.createHash('sha256').update(token.trim()).digest('hex');
    const result = await db.query(
      `SELECT id, invited_email, status, created_at, expires_at FROM admin_invitations WHERE token_hash = $1`,
      [tokenHash]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({
        valid: false,
        reason: 'INVALID',
        message: 'This invitation link is invalid or has been removed. Please contact an admin for a new invitation.'
      });
    }

    const invite = result.rows[0];

    if (invite.status === 'CANCELLED') {
      return res.status(410).json({
        valid: false,
        reason: 'CANCELLED',
        message: 'This invitation was cancelled by an administrator. Please contact an admin for a new invitation.'
      });
    }

    if (invite.status === 'ACCEPTED') {
      return res.status(410).json({
        valid: false,
        reason: 'ALREADY_USED',
        message: 'This invitation has already been used. Please sign in with your Google account.'
      });
    }

    if (new Date(invite.expires_at) < new Date()) {
      await db.query(`UPDATE admin_invitations SET status = 'EXPIRED' WHERE id = $1`, [invite.id]);
      return res.status(410).json({
        valid: false,
        reason: 'EXPIRED',
        message: 'This invitation link has expired (links expire after 24 hours). Please contact an admin for a new invitation.'
      });
    }

    return res.json({
      valid: true,
      invitedEmail: invite.invited_email,
      expiresAt: invite.expires_at,
    });
  } catch (err) {
    console.error('[ADMIN VERIFY INVITE ERROR]', err);
    return res.status(500).json({ valid: false, error: 'SERVER_ERROR', message: 'Unable to verify invitation.' });
  }
});

// POST /api/v1/admin/invitations/accept
router.post('/invitations/accept', async (req, res) => {
  try {
    const { token, id_token } = req.body;
    if (!token || !id_token) {
      return res.status(400).json({ success: false, error: 'MISSING_DATA', message: 'Token and Google authentication required.' });
    }

    const tokenHash = crypto.createHash('sha256').update(token.trim()).digest('hex');
    const inviteRes = await db.query(
      `SELECT * FROM admin_invitations WHERE token_hash = $1`,
      [tokenHash]
    );

    if (inviteRes.rows.length === 0) {
      return res.status(404).json({ success: false, error: 'INVALID_INVITATION', message: 'Invitation link is invalid.' });
    }

    const invite = inviteRes.rows[0];

    if (invite.status !== 'PENDING' || new Date(invite.expires_at) < new Date()) {
      return res.status(410).json({
        success: false,
        error: 'INVITATION_INACTIVE',
        message: 'This invitation is expired, cancelled, or already used. Please contact an admin for a new invitation.'
      });
    }

    // Verify Google ID Token
    const googleUser = await verifyGoogleIdToken(id_token);
    const googleEmail = googleUser.email.toLowerCase().trim();
    const invitedEmail = invite.invited_email.toLowerCase().trim();

    // Strict Security Constraint: Recipient Google email must match the invited email
    if (googleEmail !== invitedEmail) {
      return res.status(403).json({
        success: false,
        error: 'EMAIL_MISMATCH',
        message: `Google account email (${googleEmail}) does not match the invited address (${invitedEmail}). You must sign in using ${invitedEmail}.`
      });
    }

    // Upsert user with ADMIN role
    const upsertSql = `
      INSERT INTO users (google_sub, email, full_name, profile_image, role, enrollment_status)
      VALUES ($1, $2, $3, $4, 'ADMIN', 'ACTIVE')
      ON CONFLICT (email) DO UPDATE
      SET google_sub = COALESCE(EXCLUDED.google_sub, users.google_sub),
          full_name = EXCLUDED.full_name,
          profile_image = COALESCE(EXCLUDED.profile_image, users.profile_image),
          role = 'ADMIN',
          updated_at = NOW()
      RETURNING id, email, full_name, role, enrollment_status, profile_image;
    `;
    const userRes = await db.query(upsertSql, [
      googleUser.google_sub,
      googleEmail,
      googleUser.name,
      googleUser.picture,
    ]);
    const user = userRes.rows[0];

    // Mark invitation accepted
    await db.query(
      `UPDATE admin_invitations SET status = 'ACCEPTED', accepted_at = NOW(), accepted_by = $1 WHERE id = $2`,
      [user.id, invite.id]
    );

    // Mint admin session JWT
    const sessionToken = mintSessionJwt(user);
    const isProduction = process.env.NODE_ENV === 'production';
    res.cookie('tx_session', sessionToken, {
      httpOnly: true,
      secure: isProduction,
      sameSite: isProduction ? 'None' : 'Lax',
      maxAge: 7 * 24 * 60 * 60 * 1000,
      path: '/',
    });

    return res.json({
      success: true,
      token: sessionToken,
      user: {
        id: user.id,
        email: user.email,
        fullName: user.full_name,
        role: 'ADMIN',
        enrollmentStatus: user.enrollment_status,
      },
      redirectUrl: 'admin.html',
    });
  } catch (err) {
    console.error('[ADMIN ACCEPT ERROR]', err);
    return res.status(500).json({ success: false, error: 'ACCEPT_FAILED', message: err.message });
  }
});

// ---------------------------------------------------------------------
// AUTHENTICATED ADMIN CONSOLE ENDPOINTS
// ---------------------------------------------------------------------

// GET /api/v1/admin/overview
router.get('/overview', requireAdmin, async (req, res) => {
  try {
    // 1. Key Metrics
    const studentCountRes = await db.query(`SELECT COUNT(*) FROM users WHERE role = 'STUDENT'`);
    const activeCountRes = await db.query(`SELECT COUNT(*) FROM users WHERE enrollment_status = 'ACTIVE'`);
    const completedCountRes = await db.query(`SELECT COUNT(*) FROM users WHERE enrollment_status = 'COMPLETED'`);
    const revenueRes = await db.query(`SELECT COALESCE(SUM(amount_cents), 0) AS total_cents FROM enrollments WHERE status = 'ACTIVE'`);

    // Accurate double-entry ledger metrics
    let ledgerStats = { grossCents: 0, feeCents: 0, netCents: 0, refundCents: 0 };
    try {
      const ledgerRes = await db.query(`
        SELECT
          COALESCE(SUM(CASE WHEN status = 'SUCCEEDED' THEN gross_amount_cents ELSE 0 END), 0) AS gross,
          COALESCE(SUM(CASE WHEN status = 'SUCCEEDED' THEN stripe_fee_cents ELSE 0 END), 0) AS fee,
          COALESCE(SUM(CASE WHEN status = 'SUCCEEDED' THEN net_amount_cents ELSE 0 END), 0) AS net,
          COALESCE(SUM(refund_amount_cents), 0) AS refund
        FROM payment_transactions
      `);
      if (ledgerRes.rows.length > 0) {
        ledgerStats = {
          grossCents: parseInt(ledgerRes.rows[0].gross || '0', 10),
          feeCents: parseInt(ledgerRes.rows[0].fee || '0', 10),
          netCents: parseInt(ledgerRes.rows[0].net || '0', 10),
          refundCents: parseInt(ledgerRes.rows[0].refund || '0', 10),
        };
      }
    } catch (_) {}

    // Partnership Stats
    const partnerCountRes = await db.query(`SELECT COUNT(*) FROM partnerships WHERE status = 'ACTIVE'`);
    const partnerRevenueRes = await db.query(`SELECT COALESCE(SUM(total_commission_cents), 0) AS total FROM partnerships`);

    // 2. Active Admins
    const adminsRes = await db.query(`
      SELECT id, email, full_name, role, created_at, updated_at
      FROM users
      WHERE role = 'ADMIN' OR LOWER(email) = LOWER(PRIMARY_ADMIN_EMAIL)
      ORDER BY created_at ASC
    `);

    // 3. Admin Invitations (auto-mark expired)
    await db.query(`
      UPDATE admin_invitations
      SET status = 'EXPIRED'
      WHERE status = 'PENDING' AND expires_at < NOW()
    `);

    const invitesRes = await db.query(`
      SELECT id, invited_email, status, created_at, expires_at, accepted_at
      FROM admin_invitations
      ORDER BY created_at DESC
      LIMIT 50
    `);

    // 4. Recent Students
    const recentStudentsRes = await db.query(`
      SELECT id, email, full_name, enrollment_status, created_at
      FROM users
      WHERE role = 'STUDENT'
      ORDER BY created_at DESC
      LIMIT 10
    `);

    return res.json({
      success: true,
      stats: {
        totalStudents: parseInt(studentCountRes.rows[0]?.count || '0', 10),
        activeEnrollments: parseInt(activeCountRes.rows[0]?.count || '0', 10),
        completedCourses: parseInt(completedCountRes.rows[0]?.count || '0', 10),
        totalRevenueCents: parseInt(revenueRes.rows[0]?.total_cents || '0', 10),
        ledger: ledgerStats,
      },
      partnershipStats: {
        activePartners: parseInt(partnerCountRes.rows[0]?.count || '0', 10),
        totalCommissionCents: parseInt(partnerRevenueRes.rows[0]?.total || '0', 10),
      },
      admins: adminsRes.rows.map(a => ({
        id: a.id,
        email: a.email,
        fullName: a.full_name || a.email.split('@')[0],
        role: SUPER_ADMIN_EMAILS.includes((a.email || '').toLowerCase()) ? 'SUPER ADMIN' : 'ADMIN',
        createdAt: a.created_at,
      })),
      invitations: invitesRes.rows.map(inv => ({
        id: inv.id,
        email: inv.invited_email,
        status: inv.status,
        createdAt: inv.created_at,
        expiresAt: inv.expires_at,
        acceptedAt: inv.accepted_at,
      })),
      recentStudents: recentStudentsRes.rows,
      pricing: await getPricing(),
    });
  } catch (err) {
    console.error('[ADMIN OVERVIEW ERROR]', err);
    return res.status(500).json({ success: false, error: 'OVERVIEW_ERROR', message: err.message });
  }
});

// POST /api/v1/admin/invitations (Send Access)
router.post('/invitations', requireAdmin, async (req, res) => {
  try {
    const { email, clientOrigin } = req.body;
    if (!email) {
      return res.status(400).json({ success: false, error: 'MISSING_EMAIL', message: 'Enter a valid email address.' });
    }

    const cleanEmail = email.trim().toLowerCase();
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(cleanEmail)) {
      return res.status(400).json({ success: false, error: 'INVALID_EMAIL', message: 'Enter a valid email address.' });
    }

    // 1. Check if user is the primary admin trying to invite themselves
    if (cleanEmail === PRIMARY_ADMIN_EMAIL) {
      return res.status(400).json({
        success: false,
        error: 'ALREADY_ADMIN',
        message: `${cleanEmail} is the primary admin.`
      });
    }

    // 2. Invalidate any existing pending invitations for this email
    await db.query(
      `UPDATE admin_invitations SET status = 'CANCELLED' WHERE LOWER(invited_email) = $1 AND status = 'PENDING'`,
      [cleanEmail]
    );

    // 3. Generate secure random single-use token and store SHA-256 hash
    const rawToken = crypto.randomBytes(32).toString('hex');
    const tokenHash = crypto.createHash('sha256').update(rawToken).digest('hex');

    // 4. Resolve inviting admin user ID
    let adminUserId = null;
    try {
      const userLookup = await db.query(
        `SELECT id FROM users WHERE id = $1 OR LOWER(email) = $2 LIMIT 1`,
        [req.user.id || '00000000-0000-0000-0000-000000000000', (req.user.email || '').toLowerCase()]
      );
      if (userLookup.rows.length > 0) {
        adminUserId = userLookup.rows[0].id;
      }
    } catch (_) {}

    // Insert invitation (expires in 24 hours)
    const insertRes = await db.query(
      `INSERT INTO admin_invitations (invited_email, token_hash, invited_by, status, expires_at)
       VALUES ($1, $2, $3, 'PENDING', NOW() + INTERVAL '24 hours')
       RETURNING id, invited_email, status, created_at, expires_at`,
      [cleanEmail, tokenHash, adminUserId]
    );
    const newInvite = insertRes.rows[0];

    // 5. Construct invite URL
    const returnBase = clientOrigin || process.env.CLIENT_URL || 'http://localhost:3000';
    const inviteUrl = `${returnBase}/accept-invite.html?token=${rawToken}`;

    // 6. Send transactional invitation email via Resend
    const mailRes = await sendAdminInvitationEmail({ email: cleanEmail, inviteUrl });
    const isDelivered = mailRes && mailRes.success;

    return res.json({
      success: true,
      emailSent: Boolean(isDelivered),
      inviteUrl,
      deliveryError: isDelivered ? null : (mailRes?.error || 'Email provider sandbox restricted'),
      message: isDelivered
        ? `Invitation sent to ${cleanEmail}.`
        : `Invitation created! Note: Email delivery blocked by sandbox restriction. Use the direct link below.`,
      invitation: {
        id: newInvite.id,
        email: newInvite.invited_email,
        status: newInvite.status,
        createdAt: newInvite.created_at,
        expiresAt: newInvite.expires_at,
      },
    });
  } catch (err) {
    console.error('[ADMIN INVITE ERROR]', err);
    return res.status(500).json({ success: false, error: 'INVITE_FAILED', message: err.message });
  }
});

// POST /api/v1/admin/invitations/:id/resend
router.post('/invitations/:id/resend', requireAdmin, async (req, res) => {
  try {
    const { id } = req.params;
    const { clientOrigin } = req.body;

    const currentRes = await db.query(`SELECT * FROM admin_invitations WHERE id = $1`, [id]);
    if (currentRes.rows.length === 0) {
      return res.status(404).json({ success: false, error: 'NOT_FOUND', message: 'Invitation not found.' });
    }

    const current = currentRes.rows[0];
    const cleanEmail = current.invited_email.toLowerCase().trim();

    // Invalidate old invitation
    await db.query(`UPDATE admin_invitations SET status = 'CANCELLED' WHERE id = $1`, [id]);

    // Create fresh token and 24-hour expiration
    const rawToken = crypto.randomBytes(32).toString('hex');
    const tokenHash = crypto.createHash('sha256').update(rawToken).digest('hex');

    let adminUserId = null;
    try {
      const userLookup = await db.query(
        `SELECT id FROM users WHERE id = $1 OR LOWER(email) = $2 LIMIT 1`,
        [req.user.id || '00000000-0000-0000-0000-000000000000', (req.user.email || '').toLowerCase()]
      );
      if (userLookup.rows.length > 0) {
        adminUserId = userLookup.rows[0].id;
      }
    } catch (_) {}

    const newRes = await db.query(
      `INSERT INTO admin_invitations (invited_email, token_hash, invited_by, status, expires_at)
       VALUES ($1, $2, $3, 'PENDING', NOW() + INTERVAL '24 hours')
       RETURNING id, invited_email, status, created_at, expires_at`,
      [cleanEmail, tokenHash, adminUserId]
    );
    const newInvite = newRes.rows[0];

    const returnBase = clientOrigin || process.env.CLIENT_URL || 'http://localhost:3000';
    const inviteUrl = `${returnBase}/accept-invite.html?token=${rawToken}`;

    const mailRes = await sendAdminInvitationEmail({ email: cleanEmail, inviteUrl });
    const isDelivered = mailRes && mailRes.success;

    return res.json({
      success: true,
      emailSent: Boolean(isDelivered),
      inviteUrl,
      deliveryError: isDelivered ? null : (mailRes?.error || 'Email provider sandbox restricted'),
      message: isDelivered
        ? `New invitation sent to ${cleanEmail}.`
        : `New invitation created! Note: Email delivery blocked by sandbox restriction. Use the direct link below.`,
      invitation: {
        id: newInvite.id,
        email: newInvite.invited_email,
        status: newInvite.status,
        createdAt: newInvite.created_at,
        expiresAt: newInvite.expires_at,
      },
    });
  } catch (err) {
    console.error('[ADMIN RESEND ERROR]', err);
    return res.status(500).json({ success: false, error: 'RESEND_FAILED', message: err.message });
  }
});

// POST /api/v1/admin/invitations/:id/cancel
router.post('/invitations/:id/cancel', requireAdmin, async (req, res) => {
  try {
    const { id } = req.params;
    const result = await db.query(
      `UPDATE admin_invitations SET status = 'CANCELLED' WHERE id = $1 RETURNING id, invited_email`,
      [id]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ success: false, error: 'NOT_FOUND', message: 'Invitation not found.' });
    }

    return res.json({
      success: true,
      message: `Invitation for ${result.rows[0].invited_email} was cancelled.`,
    });
  } catch (err) {
    console.error('[ADMIN CANCEL ERROR]', err);
    return res.status(500).json({ success: false, error: 'CANCEL_FAILED', message: err.message });
  }
});

// ---------------------------------------------------------------------
// PARTNERSHIP MANAGEMENT ENDPOINTS
// ---------------------------------------------------------------------

// GET /api/v1/admin/partnerships
// List all partnerships ordered by created_at DESC
router.get('/partnerships', requireAdmin, async (req, res) => {
  try {
    const result = await db.query(`SELECT * FROM partnerships ORDER BY created_at DESC`);
    return res.json(result.rows);
  } catch (err) {
    console.error('[ADMIN GET PARTNERSHIPS ERROR]', err);
    return res.status(500).json({ success: false, error: 'FETCH_PARTNERSHIPS_FAILED', message: err.message });
  }
});

// GET /api/v1/admin/partnerships/stats
// Aggregate stats: total active partners, total referrals, total revenue, total commission, total unpaid commission
router.get('/partnerships/stats', requireAdmin, async (req, res) => {
  try {
    const statsRes = await db.query(`
      SELECT
        COUNT(*) FILTER (WHERE status = 'ACTIVE') AS active_partners,
        COALESCE(SUM(total_referrals), 0) AS total_referrals,
        COALESCE(SUM(total_revenue_cents), 0) AS total_revenue_cents,
        COALESCE(SUM(total_commission_cents), 0) AS total_commission_cents,
        COALESCE(SUM(total_paid_out_cents), 0) AS total_paid_out_cents,
        COALESCE(SUM(total_commission_cents - total_paid_out_cents), 0) AS total_unpaid_commission_cents
      FROM partnerships
    `);

    const row = statsRes.rows[0] || {};
    const activePartners = parseInt(row.active_partners || '0', 10);
    const totalReferrals = parseInt(row.total_referrals || '0', 10);
    const totalRevenueCents = parseInt(row.total_revenue_cents || '0', 10);
    const totalCommissionCents = parseInt(row.total_commission_cents || '0', 10);
    const totalPaidOutCents = parseInt(row.total_paid_out_cents || '0', 10);
    const totalUnpaidCommissionCents = parseInt(row.total_unpaid_commission_cents || '0', 10);

    return res.json({
      success: true,
      activePartners,
      totalActivePartners: activePartners,
      totalReferrals,
      totalRevenueCents,
      totalRevenue: totalRevenueCents,
      totalCommissionCents,
      totalCommission: totalCommissionCents,
      totalPaidOutCents,
      totalUnpaidCommissionCents,
      totalUnpaidCommission: totalUnpaidCommissionCents,
      unpaidCommissionCents: totalUnpaidCommissionCents,
      active_partners: activePartners,
      total_referrals: totalReferrals,
      total_revenue_cents: totalRevenueCents,
      total_commission_cents: totalCommissionCents,
      total_paid_out_cents: totalPaidOutCents,
      total_unpaid_commission_cents: totalUnpaidCommissionCents,
    });
  } catch (err) {
    console.error('[ADMIN PARTNERSHIP STATS ERROR]', err);
    return res.status(500).json({ success: false, error: 'STATS_FAILED', message: err.message });
  }
});

// POST /api/v1/admin/partnerships
// Create new partnership with auto-generated referral code
router.post('/partnerships', requireAdmin, async (req, res) => {
  try {
    const {
      partnerName,
      contactName,
      contactEmail,
      contactPhone,
      commissionPercent,
      notes,
    } = req.body || {};

    const pName = partnerName || req.body?.partner_name;
    const cName = contactName !== undefined ? contactName : req.body?.contact_name;
    const cEmail = contactEmail || req.body?.contact_email;
    const cPhone = contactPhone !== undefined ? contactPhone : req.body?.contact_phone;
    const cPercent = commissionPercent !== undefined ? commissionPercent : (req.body?.commission_percent !== undefined ? req.body.commission_percent : 10.00);
    const cNotes = notes !== undefined ? notes : req.body?.notes;

    if (!pName || !cEmail) {
      return res.status(400).json({
        success: false,
        error: 'MISSING_FIELDS',
        message: 'Partner name and contact email are required.'
      });
    }

    const cleanEmail = cEmail.trim().toLowerCase();
    const parsedCommission = isNaN(parseFloat(cPercent)) ? 10.00 : parseFloat(cPercent);

    // Auto-generate referral code: uppercase first word + random 4 digits (e.g. "SUNRISE4829")
    const cleanWord = pName.trim().replace(/[^a-zA-Z0-9\s]/g, '').split(/\s+/)[0] || 'PARTNER';
    const firstWord = cleanWord.toUpperCase() || 'PARTNER';

    let referralCode = '';
    let isUnique = false;
    for (let i = 0; i < 15; i++) {
      const random4 = Math.floor(1000 + Math.random() * 9000).toString();
      const candidate = `${firstWord}${random4}`;
      const checkRes = await db.query(`SELECT 1 FROM partnerships WHERE referral_code = $1`, [candidate]);
      if (checkRes.rows.length === 0) {
        referralCode = candidate;
        isUnique = true;
        break;
      }
    }

    if (!isUnique) {
      referralCode = `${firstWord}${crypto.randomBytes(2).toString('hex').toUpperCase()}`;
    }

    // Resolve admin user ID
    let adminUserId = null;
    try {
      const userLookup = await db.query(
        `SELECT id FROM users WHERE id = $1 OR LOWER(email) = $2 LIMIT 1`,
        [req.user.id || '00000000-0000-0000-0000-000000000000', (req.user.email || '').toLowerCase()]
      );
      if (userLookup.rows.length > 0) {
        adminUserId = userLookup.rows[0].id;
      }
    } catch (_) {}

    // Insert partnership
    const insertRes = await db.query(
      `INSERT INTO partnerships (
        partner_name,
        contact_name,
        contact_email,
        contact_phone,
        referral_code,
        commission_percent,
        status,
        notes,
        created_by
      )
      VALUES ($1, $2, $3, $4, $5, $6, 'ACTIVE', $7, $8)
      RETURNING *`,
      [
        pName.trim(),
        cName ? cName.trim() : null,
        cleanEmail,
        cPhone ? cPhone.trim() : null,
        referralCode,
        parsedCommission,
        cNotes || null,
        adminUserId,
      ]
    );

    const created = insertRes.rows[0];

    // Auto-create a PARTNER coupon for this referral code
    try {
      await db.query(
        `INSERT INTO coupons (code, type, partnership_id, discount_type, discount_value, created_by)
         VALUES ($1, 'PARTNER', $2, 'NONE', 0, $3)
         ON CONFLICT (code) DO NOTHING`,
        [referralCode, created.id, adminUserId]
      );
    } catch (couponErr) {
      console.warn('[AUTO-COUPON]', couponErr.message);
    }

    // Auto-generate portal access key
    let portalUrl = null;
    try {
      const rawKey = crypto.randomBytes(32).toString('hex');
      const keyHash = crypto.createHash('sha256').update(rawKey).digest('hex');
      await db.query(
        `INSERT INTO partner_access_keys (partnership_id, key_hash, is_active) VALUES ($1, $2, true)`,
        [created.id, keyHash]
      );
      const portalBase = req.body.clientOrigin || process.env.CLIENT_URL || 'http://localhost:3000';
      portalUrl = `${portalBase}/partner.html?key=${rawKey}`;
    } catch (keyErr) {
      console.warn('[AUTO-PORTAL-KEY]', keyErr.message);
    }

    return res.status(201).json({
      success: true,
      partnership: created,
      portalUrl,
      ...created,
    });
  } catch (err) {
    console.error('[ADMIN CREATE PARTNERSHIP ERROR]', err);
    return res.status(500).json({ success: false, error: 'CREATE_PARTNERSHIP_FAILED', message: err.message });
  }
});

// PUT /api/v1/admin/partnerships/:id
// Update partnership fields
router.put('/partnerships/:id', requireAdmin, async (req, res) => {
  try {
    const { id } = req.params;
    const body = req.body || {};

    const partnerName = body.partnerName !== undefined ? body.partnerName : body.partner_name;
    const contactName = body.contactName !== undefined ? body.contactName : body.contact_name;
    const contactEmail = body.contactEmail !== undefined ? body.contactEmail : body.contact_email;
    const contactPhone = body.contactPhone !== undefined ? body.contactPhone : body.contact_phone;
    const commissionPercent = body.commissionPercent !== undefined ? body.commissionPercent : body.commission_percent;
    const notes = body.notes !== undefined ? body.notes : undefined;
    const status = body.status !== undefined ? body.status : undefined;

    const updates = [];
    const values = [];
    let idx = 1;

    if (partnerName !== undefined) {
      updates.push(`partner_name = $${idx++}`);
      values.push(partnerName.trim());
    }
    if (contactName !== undefined) {
      updates.push(`contact_name = $${idx++}`);
      values.push(contactName ? contactName.trim() : null);
    }
    if (contactEmail !== undefined) {
      updates.push(`contact_email = $${idx++}`);
      values.push(contactEmail.trim().toLowerCase());
    }
    if (contactPhone !== undefined) {
      updates.push(`contact_phone = $${idx++}`);
      values.push(contactPhone ? contactPhone.trim() : null);
    }
    if (commissionPercent !== undefined) {
      updates.push(`commission_percent = $${idx++}`);
      values.push(parseFloat(commissionPercent));
    }
    if (notes !== undefined) {
      updates.push(`notes = $${idx++}`);
      values.push(notes);
    }
    if (status !== undefined) {
      updates.push(`status = $${idx++}`);
      values.push(status);
    }

    if (updates.length === 0) {
      return res.status(400).json({ success: false, error: 'NO_UPDATES', message: 'No fields provided for update.' });
    }

    updates.push(`updated_at = NOW()`);
    values.push(id);

    const queryText = `
      UPDATE partnerships
      SET ${updates.join(', ')}
      WHERE id = $${idx}
      RETURNING *
    `;

    const result = await db.query(queryText, values);
    if (result.rows.length === 0) {
      return res.status(404).json({ success: false, error: 'NOT_FOUND', message: 'Partnership not found.' });
    }

    const updated = result.rows[0];
    return res.json({
      success: true,
      partnership: updated,
      ...updated,
    });
  } catch (err) {
    console.error('[ADMIN UPDATE PARTNERSHIP ERROR]', err);
    return res.status(500).json({ success: false, error: 'UPDATE_FAILED', message: err.message });
  }
});

// POST /api/v1/admin/partnerships/:id/toggle
// Toggle status between 'ACTIVE' and 'PAUSED'
router.post('/partnerships/:id/toggle', requireAdmin, async (req, res) => {
  try {
    const { id } = req.params;
    const currentRes = await db.query(`SELECT id, status FROM partnerships WHERE id = $1`, [id]);
    if (currentRes.rows.length === 0) {
      return res.status(404).json({ success: false, error: 'NOT_FOUND', message: 'Partnership not found.' });
    }

    const currentStatus = currentRes.rows[0].status;
    const newStatus = currentStatus === 'ACTIVE' ? 'PAUSED' : 'ACTIVE';

    const updateRes = await db.query(
      `UPDATE partnerships SET status = $1, updated_at = NOW() WHERE id = $2 RETURNING *`,
      [newStatus, id]
    );

    const updated = updateRes.rows[0];
    return res.json({
      success: true,
      message: `Partnership status toggled to ${newStatus}.`,
      status: newStatus,
      partnership: updated,
      ...updated,
    });
  } catch (err) {
    console.error('[ADMIN PARTNERSHIP TOGGLE ERROR]', err);
    return res.status(500).json({ success: false, error: 'TOGGLE_FAILED', message: err.message });
  }
});

// DELETE /api/v1/admin/partnerships/:id
// Soft delete - set status to 'TERMINATED'
router.delete('/partnerships/:id', requireAdmin, async (req, res) => {
  try {
    const { id } = req.params;
    const result = await db.query(
      `UPDATE partnerships SET status = 'TERMINATED', updated_at = NOW() WHERE id = $1 RETURNING *`,
      [id]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ success: false, error: 'NOT_FOUND', message: 'Partnership not found.' });
    }

    const terminated = result.rows[0];
    return res.json({
      success: true,
      message: 'Partnership terminated successfully.',
      status: 'TERMINATED',
      partnership: terminated,
      ...terminated,
    });
  } catch (err) {
    console.error('[ADMIN PARTNERSHIP DELETE ERROR]', err);
    return res.status(500).json({ success: false, error: 'DELETE_FAILED', message: err.message });
  }
});

// GET /api/v1/admin/partnerships/:id/referrals
// Get all referrals for a specific partnership
router.get('/partnerships/:id/referrals', requireAdmin, async (req, res) => {
  try {
    const { id } = req.params;
    const partnerCheck = await db.query(`SELECT id FROM partnerships WHERE id = $1`, [id]);
    if (partnerCheck.rows.length === 0) {
      return res.status(404).json({ success: false, error: 'NOT_FOUND', message: 'Partnership not found.' });
    }

    const result = await db.query(
      `SELECT pr.*, u.email AS user_email, u.full_name AS user_name
       FROM partnership_referrals pr
       LEFT JOIN users u ON u.id = pr.user_id
       WHERE pr.partnership_id = $1
       ORDER BY pr.created_at DESC`,
      [id]
    );

    return res.json(result.rows);
  } catch (err) {
    console.error('[ADMIN GET PARTNERSHIP REFERRALS ERROR]', err);
    return res.status(500).json({ success: false, error: 'REFERRALS_FETCH_FAILED', message: err.message });
  }
});

// ---------------------------------------------------------------------
// STUDENT MANAGEMENT ENDPOINTS
// ---------------------------------------------------------------------

// GET /api/v1/admin/students
// Paginated student list with filtering by search and status
router.get('/students', requireAdmin, async (req, res) => {
  try {
    const page = Math.max(1, parseInt(req.query.page, 10) || 1);
    const limit = Math.max(1, Math.min(100, parseInt(req.query.limit, 10) || 25));
    const offset = (page - 1) * limit;

    const search = req.query.search ? String(req.query.search).trim() : '';
    const status = req.query.status ? String(req.query.status).trim() : '';

    const conditions = [`role = 'STUDENT'`];
    const params = [];
    let pIdx = 1;

    if (search) {
      conditions.push(`(LOWER(email) LIKE $${pIdx} OR LOWER(full_name) LIKE $${pIdx})`);
      params.push(`%${search.toLowerCase()}%`);
      pIdx++;
    }

    if (status) {
      conditions.push(`enrollment_status = $${pIdx}`);
      params.push(status);
      pIdx++;
    }

    const whereClause = conditions.join(' AND ');

    // Total count query
    const countRes = await db.query(
      `SELECT COUNT(*) FROM users WHERE ${whereClause}`,
      params
    );
    const total = parseInt(countRes.rows[0]?.count || '0', 10);
    const totalPages = Math.ceil(total / limit) || (total === 0 ? 0 : 1);

    // Paginated records query
    const dataParams = [...params, limit, offset];
    const studentsRes = await db.query(
      `SELECT id, email, full_name, enrollment_status, role, created_at, updated_at
       FROM users
       WHERE ${whereClause}
       ORDER BY created_at DESC
       LIMIT $${pIdx} OFFSET $${pIdx + 1}`,
      dataParams
    );

    return res.json({
      success: true,
      students: studentsRes.rows,
      total,
      page,
      totalPages,
      limit,
    });
  } catch (err) {
    console.error('[ADMIN GET STUDENTS ERROR]', err);
    return res.status(500).json({ success: false, error: 'STUDENTS_FETCH_FAILED', message: err.message });
  }
});

// ---------------------------------------------------------------------
// COUPON MANAGEMENT ENDPOINTS
// ---------------------------------------------------------------------

// GET /api/v1/admin/coupons
router.get('/coupons', requireAdmin, async (req, res) => {
  try {
    const result = await db.query(
      `SELECT c.*, p.partner_name
       FROM coupons c
       LEFT JOIN partnerships p ON p.id = c.partnership_id
       ORDER BY c.created_at DESC`
    );
    return res.json({ success: true, coupons: result.rows });
  } catch (err) {
    console.error('[ADMIN GET COUPONS ERROR]', err);
    return res.status(500).json({ success: false, error: 'FETCH_COUPONS_FAILED', message: err.message });
  }
});

// POST /api/v1/admin/coupons
router.post('/coupons', requireAdmin, async (req, res) => {
  try {
    const { code, discountType, discountValue, maxUses, expiresAt } = req.body;
    if (!code) {
      return res.status(400).json({ success: false, error: 'MISSING_CODE', message: 'Coupon code is required.' });
    }
    const cleanCode = code.trim().toUpperCase();

    // Check uniqueness
    const exists = await db.query(`SELECT 1 FROM coupons WHERE code = $1`, [cleanCode]);
    if (exists.rows.length > 0) {
      return res.status(400).json({ success: false, error: 'DUPLICATE_CODE', message: 'This coupon code already exists.' });
    }

    let adminUserId = null;
    try {
      const userLookup = await db.query(
        `SELECT id FROM users WHERE id = $1 OR LOWER(email) = $2 LIMIT 1`,
        [req.user.id || '00000000-0000-0000-0000-000000000000', (req.user.email || '').toLowerCase()]
      );
      if (userLookup.rows.length > 0) adminUserId = userLookup.rows[0].id;
    } catch (_) {}

    const result = await db.query(
      `INSERT INTO coupons (code, type, discount_type, discount_value, max_uses, expires_at, created_by)
       VALUES ($1, 'PROMO', $2, $3, $4, $5, $6)
       RETURNING *`,
      [cleanCode, discountType || 'PERCENT', parseFloat(discountValue) || 0, maxUses || null, expiresAt || null, adminUserId]
    );
    return res.status(201).json({ success: true, coupon: result.rows[0] });
  } catch (err) {
    console.error('[ADMIN CREATE COUPON ERROR]', err);
    return res.status(500).json({ success: false, error: 'CREATE_COUPON_FAILED', message: err.message });
  }
});

// PUT /api/v1/admin/coupons/:id
router.put('/coupons/:id', requireAdmin, async (req, res) => {
  try {
    const { id } = req.params;
    const { discountType, discountValue, maxUses, expiresAt, isActive } = req.body;
    const updates = [];
    const values = [];
    let idx = 1;

    if (discountType !== undefined) { updates.push(`discount_type = $${idx++}`); values.push(discountType); }
    if (discountValue !== undefined) { updates.push(`discount_value = $${idx++}`); values.push(parseFloat(discountValue)); }
    if (maxUses !== undefined) { updates.push(`max_uses = $${idx++}`); values.push(maxUses); }
    if (expiresAt !== undefined) { updates.push(`expires_at = $${idx++}`); values.push(expiresAt); }
    if (isActive !== undefined) { updates.push(`is_active = $${idx++}`); values.push(isActive); }

    if (updates.length === 0) {
      return res.status(400).json({ success: false, error: 'NO_UPDATES', message: 'No fields provided.' });
    }
    updates.push(`updated_at = NOW()`);
    values.push(id);

    const result = await db.query(
      `UPDATE coupons SET ${updates.join(', ')} WHERE id = $${idx} RETURNING *`,
      values
    );
    if (result.rows.length === 0) {
      return res.status(404).json({ success: false, error: 'NOT_FOUND', message: 'Coupon not found.' });
    }
    return res.json({ success: true, coupon: result.rows[0] });
  } catch (err) {
    console.error('[ADMIN UPDATE COUPON ERROR]', err);
    return res.status(500).json({ success: false, error: 'UPDATE_COUPON_FAILED', message: err.message });
  }
});

// DELETE /api/v1/admin/coupons/:id (deactivate)
router.delete('/coupons/:id', requireAdmin, async (req, res) => {
  try {
    const result = await db.query(
      `UPDATE coupons SET is_active = false, updated_at = NOW() WHERE id = $1 RETURNING *`,
      [req.params.id]
    );
    if (result.rows.length === 0) {
      return res.status(404).json({ success: false, error: 'NOT_FOUND', message: 'Coupon not found.' });
    }
    return res.json({ success: true, message: 'Coupon deactivated.' });
  } catch (err) {
    console.error('[ADMIN DELETE COUPON ERROR]', err);
    return res.status(500).json({ success: false, error: 'DELETE_COUPON_FAILED', message: err.message });
  }
});

// ---------------------------------------------------------------------
// WITHDRAWAL MANAGEMENT ENDPOINTS
// ---------------------------------------------------------------------

// GET /api/v1/admin/withdrawals
router.get('/withdrawals', requireAdmin, async (req, res) => {
  try {
    const result = await db.query(
      `SELECT wr.*, p.partner_name, p.contact_email
       FROM withdrawal_requests wr
       JOIN partnerships p ON p.id = wr.partnership_id
       ORDER BY
         CASE wr.status WHEN 'PENDING' THEN 0 WHEN 'APPROVED' THEN 1 ELSE 2 END,
         wr.created_at DESC
       LIMIT 200`
    );
    return res.json({ success: true, withdrawals: result.rows });
  } catch (err) {
    console.error('[ADMIN GET WITHDRAWALS ERROR]', err);
    return res.status(500).json({ success: false, error: 'FETCH_WITHDRAWALS_FAILED', message: err.message });
  }
});

// POST /api/v1/admin/withdrawals/:id/approve
router.post('/withdrawals/:id/approve', requireAdmin, async (req, res) => {
  try {
    let adminUserId = null;
    try {
      const ul = await db.query(`SELECT id FROM users WHERE LOWER(email) = $1 LIMIT 1`, [(req.user.email || '').toLowerCase()]);
      if (ul.rows.length > 0) adminUserId = ul.rows[0].id;
    } catch (_) {}

    const result = await db.query(
      `UPDATE withdrawal_requests SET status = 'APPROVED', reviewed_by = $1, reviewed_at = NOW()
       WHERE id = $2 AND status = 'PENDING' RETURNING *`,
      [adminUserId, req.params.id]
    );
    if (result.rows.length === 0) {
      return res.status(404).json({ success: false, message: 'Withdrawal not found or already processed.' });
    }
    return res.json({ success: true, withdrawal: result.rows[0], message: 'Withdrawal approved.' });
  } catch (err) {
    console.error('[ADMIN APPROVE WITHDRAWAL ERROR]', err);
    return res.status(500).json({ success: false, error: 'APPROVE_FAILED', message: err.message });
  }
});

// POST /api/v1/admin/withdrawals/:id/reject
router.post('/withdrawals/:id/reject', requireAdmin, async (req, res) => {
  try {
    const { reason } = req.body;
    let adminUserId = null;
    try {
      const ul = await db.query(`SELECT id FROM users WHERE LOWER(email) = $1 LIMIT 1`, [(req.user.email || '').toLowerCase()]);
      if (ul.rows.length > 0) adminUserId = ul.rows[0].id;
    } catch (_) {}

    const result = await db.query(
      `UPDATE withdrawal_requests SET status = 'REJECTED', admin_notes = $1, reviewed_by = $2, reviewed_at = NOW()
       WHERE id = $3 AND status IN ('PENDING', 'APPROVED') RETURNING *`,
      [reason || 'Rejected by admin', adminUserId, req.params.id]
    );
    if (result.rows.length === 0) {
      return res.status(404).json({ success: false, message: 'Withdrawal not found or already processed.' });
    }
    return res.json({ success: true, withdrawal: result.rows[0], message: 'Withdrawal rejected.' });
  } catch (err) {
    console.error('[ADMIN REJECT WITHDRAWAL ERROR]', err);
    return res.status(500).json({ success: false, error: 'REJECT_FAILED', message: err.message });
  }
});

// POST /api/v1/admin/withdrawals/:id/paid
router.post('/withdrawals/:id/paid', requireAdmin, async (req, res) => {
  try {
    const wr = await db.query(`SELECT * FROM withdrawal_requests WHERE id = $1`, [req.params.id]);
    if (wr.rows.length === 0 || !['PENDING', 'APPROVED'].includes(wr.rows[0].status)) {
      return res.status(404).json({ success: false, message: 'Withdrawal not found or not payable.' });
    }

    let adminUserId = null;
    try {
      const ul = await db.query(`SELECT id FROM users WHERE LOWER(email) = $1 LIMIT 1`, [(req.user.email || '').toLowerCase()]);
      if (ul.rows.length > 0) adminUserId = ul.rows[0].id;
    } catch (_) {}

    // Mark as paid
    await db.query(
      `UPDATE withdrawal_requests SET status = 'PAID', paid_at = NOW(), reviewed_by = $1, reviewed_at = NOW()
       WHERE id = $2`,
      [adminUserId, req.params.id]
    );

    // Update partnership paid out total
    await db.query(
      `UPDATE partnerships SET total_paid_out_cents = total_paid_out_cents + $1, updated_at = NOW()
       WHERE id = $2`,
      [wr.rows[0].amount_cents, wr.rows[0].partnership_id]
    );

    return res.json({ success: true, message: 'Withdrawal marked as paid. Partner total_paid_out updated.' });
  } catch (err) {
    console.error('[ADMIN PAID WITHDRAWAL ERROR]', err);
    return res.status(500).json({ success: false, error: 'PAID_FAILED', message: err.message });
  }
});

// ---------------------------------------------------------------------
// PARTNER PORTAL KEY MANAGEMENT
// ---------------------------------------------------------------------

// POST /api/v1/admin/partnerships/:id/portal-key
router.post('/partnerships/:id/portal-key', requireAdmin, async (req, res) => {
  try {
    const { id } = req.params;
    const partnerCheck = await db.query(`SELECT id, partner_name FROM partnerships WHERE id = $1`, [id]);
    if (partnerCheck.rows.length === 0) {
      return res.status(404).json({ success: false, message: 'Partnership not found.' });
    }

    // Deactivate existing keys
    await db.query(`UPDATE partner_access_keys SET is_active = false WHERE partnership_id = $1`, [id]);

    // Generate new key
    const rawKey = crypto.randomBytes(32).toString('hex');
    const keyHash = crypto.createHash('sha256').update(rawKey).digest('hex');

    await db.query(
      `INSERT INTO partner_access_keys (partnership_id, key_hash, is_active) VALUES ($1, $2, true)`,
      [id, keyHash]
    );

    const portalBase = req.body.clientOrigin || process.env.CLIENT_URL || 'http://localhost:3000';
    const portalUrl = `${portalBase}/partner.html?key=${rawKey}`;

    return res.json({
      success: true,
      portalKey: rawKey,
      portalUrl,
      message: `Portal link generated for ${partnerCheck.rows[0].partner_name}. Share this link with the partner.`,
    });
  } catch (err) {
    console.error('[ADMIN PORTAL KEY ERROR]', err);
    return res.status(500).json({ success: false, error: 'PORTAL_KEY_FAILED', message: err.message });
  }
});

// ---------------------------------------------------------------------
// PRICING MANAGEMENT (ADMIN)
// ---------------------------------------------------------------------

// GET /api/v1/admin/pricing
router.get('/pricing', requireAdmin, async (req, res) => {
  try {
    const pricing = await getPricing();
    const configRes = await db.query(
      `SELECT p.*, u.email AS updated_by_email, u.full_name AS updated_by_name
       FROM pricing_config p
       LEFT JOIN users u ON u.id = p.updated_by
       WHERE p.id = 'default'`
    );
    const row = configRes.rows[0] || {};
    return res.json({
      success: true,
      pricing: {
        ...pricing,
        updatedBy: row.updated_by_email || row.updated_by_name || 'System Default',
      }
    });
  } catch (err) {
    console.error('[ADMIN GET PRICING ERROR]', err);
    return res.status(500).json({ success: false, error: 'PRICING_FETCH_FAILED', message: err.message });
  }
});

// GET /api/v1/admin/transactions
// Full double-entry financial audit ledger for 100% accurate accounting
router.get('/transactions', requireAdmin, async (req, res) => {
  try {
    const limit = Math.min(parseInt(req.query.limit || '50', 10), 200);
    const offset = parseInt(req.query.offset || '0', 10);

    const txRes = await db.query(
      `SELECT t.*, u.full_name AS user_full_name
       FROM payment_transactions t
       LEFT JOIN users u ON u.id = t.user_id
       ORDER BY t.created_at DESC
       LIMIT $1 OFFSET $2`,
      [limit, offset]
    );

    const summaryRes = await db.query(
      `SELECT
         COUNT(*) AS total_count,
         COALESCE(SUM(CASE WHEN status = 'SUCCEEDED' THEN gross_amount_cents ELSE 0 END), 0) AS total_gross_cents,
         COALESCE(SUM(CASE WHEN status = 'SUCCEEDED' THEN stripe_fee_cents ELSE 0 END), 0) AS total_fee_cents,
         COALESCE(SUM(CASE WHEN status = 'SUCCEEDED' THEN net_amount_cents ELSE 0 END), 0) AS total_net_cents,
         COALESCE(SUM(refund_amount_cents), 0) AS total_refund_cents
       FROM payment_transactions`
    );

    const s = summaryRes.rows[0] || {};
    return res.json({
      success: true,
      transactions: txRes.rows,
      summary: {
        totalCount: parseInt(s.total_count || '0', 10),
        totalGrossCents: parseInt(s.total_gross_cents || '0', 10),
        totalFeeCents: parseInt(s.total_fee_cents || '0', 10),
        totalNetCents: parseInt(s.total_net_cents || '0', 10),
        totalRefundCents: parseInt(s.total_refund_cents || '0', 10),
      }
    });
  } catch (err) {
    console.error('[ADMIN GET TRANSACTIONS ERROR]', err);
    return res.status(500).json({ success: false, error: 'FETCH_TRANSACTIONS_FAILED', message: err.message });
  }
});

// PUT /api/v1/admin/pricing
router.put('/pricing', requireAdmin, async (req, res) => {
  try {
    const { coursePrice, rushPrice, coursePriceCents, rushPriceCents } = req.body;

    // Support either decimal dollars ($38.00) or cents (3800)
    let finalCourseCents = null;
    let finalRushCents = null;

    if (coursePriceCents !== undefined && coursePriceCents !== null) {
      finalCourseCents = parseInt(coursePriceCents, 10);
    } else if (coursePrice !== undefined && coursePrice !== null) {
      finalCourseCents = Math.round(parseFloat(coursePrice) * 100);
    }

    if (rushPriceCents !== undefined && rushPriceCents !== null) {
      finalRushCents = parseInt(rushPriceCents, 10);
    } else if (rushPrice !== undefined && rushPrice !== null) {
      finalRushCents = Math.round(parseFloat(rushPrice) * 100);
    }

    if (finalCourseCents === null || isNaN(finalCourseCents) || finalCourseCents < 100) {
      return res.status(400).json({
        success: false,
        error: 'INVALID_COURSE_PRICE',
        message: 'Course price must be at least $1.00.'
      });
    }

    if (finalRushCents === null || isNaN(finalRushCents) || finalRushCents < 0) {
      return res.status(400).json({
        success: false,
        error: 'INVALID_RUSH_PRICE',
        message: 'Certificate rush delivery price cannot be negative.'
      });
    }

    // Resolve admin user ID
    let adminUserId = null;
    try {
      const userLookup = await db.query(
        `SELECT id FROM users WHERE id = $1 OR LOWER(email) = $2 LIMIT 1`,
        [req.user.id || '00000000-0000-0000-0000-000000000000', (req.user.email || '').toLowerCase()]
      );
      if (userLookup.rows.length > 0) adminUserId = userLookup.rows[0].id;
    } catch (_) {}

    await db.query(
      `INSERT INTO pricing_config (id, course_price_cents, rush_certificate_price_cents, updated_at, updated_by)
       VALUES ('default', $1, $2, NOW(), $3)
       ON CONFLICT (id) DO UPDATE
       SET course_price_cents = EXCLUDED.course_price_cents,
           rush_certificate_price_cents = EXCLUDED.rush_certificate_price_cents,
           updated_at = NOW(),
           updated_by = EXCLUDED.updated_by`,
      [finalCourseCents, finalRushCents, adminUserId]
    );

    invalidatePricingCache();
    const updated = await getPricing();

    return res.json({
      success: true,
      pricing: updated,
      message: `Pricing updated successfully! Course: ${updated.coursePriceFormatted}, Rush Certificate: ${updated.rushPriceFormatted}.`
    });
  } catch (err) {
    console.error('[ADMIN UPDATE PRICING ERROR]', err);
    return res.status(500).json({ success: false, error: 'PRICING_UPDATE_FAILED', message: err.message });
  }
});

module.exports = router;
