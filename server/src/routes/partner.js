const express = require('express');
const router = express.Router();
const crypto = require('crypto');
const db = require('../db');

// ── Partner Key Auth Middleware ──
async function requirePartnerKey(req, res, next) {
  const key = req.query.key || req.body?.key;
  if (!key) {
    return res.status(404).json({ success: false, error: 'NOT_FOUND' });
  }
  const keyHash = crypto.createHash('sha256').update(key.trim()).digest('hex');
  try {
    const result = await db.query(
      `SELECT pak.partnership_id, p.*
       FROM partner_access_keys pak
       JOIN partnerships p ON p.id = pak.partnership_id
       WHERE pak.key_hash = $1 AND pak.is_active = true AND p.status != 'TERMINATED'`,
      [keyHash]
    );
    if (result.rows.length === 0) {
      return res.status(404).json({ success: false, error: 'INVALID_KEY', message: 'Invalid or deactivated portal link. Contact your admin for a new link.' });
    }
    req.partner = result.rows[0];
    next();
  } catch (err) {
    console.error('[PARTNER AUTH ERROR]', err);
    return res.status(500).json({ success: false, error: 'AUTH_ERROR' });
  }
}

// GET /api/v1/partner/dashboard?key=...
router.get('/dashboard', requirePartnerKey, async (req, res) => {
  try {
    const p = req.partner;

    // Calculate pending withdrawal total
    const pendingRes = await db.query(
      `SELECT COALESCE(SUM(amount_cents), 0) AS total
       FROM withdrawal_requests
       WHERE partnership_id = $1 AND status IN ('PENDING', 'APPROVED')`,
      [p.id]
    );
    const pendingCents = parseInt(pendingRes.rows[0]?.total || '0', 10);
    const availableBalanceCents = Math.max(0, (p.total_commission_cents || 0) - (p.total_paid_out_cents || 0) - pendingCents);

    return res.json({
      success: true,
      partner: {
        partner_name: p.partner_name,
        referral_code: p.referral_code,
        commission_percent: parseFloat(p.commission_percent),
        total_referrals: p.total_referrals || 0,
        total_conversions: p.total_conversions || 0,
        total_revenue_cents: p.total_revenue_cents || 0,
        total_commission_cents: p.total_commission_cents || 0,
        total_paid_out_cents: p.total_paid_out_cents || 0,
      },
      pendingWithdrawalCents: pendingCents,
      availableBalanceCents,
    });
  } catch (err) {
    console.error('[PARTNER DASHBOARD ERROR]', err);
    return res.status(500).json({ success: false, error: 'DASHBOARD_ERROR', message: err.message });
  }
});

// GET /api/v1/partner/referrals?key=...
router.get('/referrals', requirePartnerKey, async (req, res) => {
  try {
    const result = await db.query(
      `SELECT pr.id, pr.amount_cents, pr.commission_cents, pr.status, pr.created_at,
              u.email AS user_email
       FROM partnership_referrals pr
       LEFT JOIN users u ON u.id = pr.user_id
       WHERE pr.partnership_id = $1
       ORDER BY pr.created_at DESC
       LIMIT 200`,
      [req.partner.id]
    );

    // Mask emails for privacy
    const referrals = result.rows.map(r => ({
      id: r.id,
      user_email: maskEmail(r.user_email),
      amount_cents: r.amount_cents,
      commission_cents: r.commission_cents,
      status: r.status || 'CREDITED',
      created_at: r.created_at,
    }));

    return res.json({ success: true, referrals });
  } catch (err) {
    console.error('[PARTNER REFERRALS ERROR]', err);
    return res.status(500).json({ success: false, error: 'REFERRALS_ERROR', message: err.message });
  }
});

// POST /api/v1/partner/withdrawals
router.post('/withdrawals', requirePartnerKey, async (req, res) => {
  try {
    const { amount_cents, payment_method, payment_details } = req.body;
    const p = req.partner;

    if (!amount_cents || amount_cents < 1000) {
      return res.status(400).json({ success: false, error: 'MIN_AMOUNT', message: 'Minimum withdrawal amount is $10.00.' });
    }
    if (!payment_method) {
      return res.status(400).json({ success: false, error: 'MISSING_METHOD', message: 'Payment method is required.' });
    }
    if (!payment_details) {
      return res.status(400).json({ success: false, error: 'MISSING_DETAILS', message: 'Payment details are required.' });
    }

    // Check available balance
    const pendingRes = await db.query(
      `SELECT COALESCE(SUM(amount_cents), 0) AS total
       FROM withdrawal_requests
       WHERE partnership_id = $1 AND status IN ('PENDING', 'APPROVED')`,
      [p.id]
    );
    const pendingCents = parseInt(pendingRes.rows[0]?.total || '0', 10);
    const available = Math.max(0, (p.total_commission_cents || 0) - (p.total_paid_out_cents || 0) - pendingCents);

    if (amount_cents > available) {
      return res.status(400).json({ success: false, error: 'INSUFFICIENT_BALANCE', message: `Insufficient balance. Available: $${(available / 100).toFixed(2)}` });
    }

    const result = await db.query(
      `INSERT INTO withdrawal_requests (partnership_id, amount_cents, status, payment_method, payment_details)
       VALUES ($1, $2, 'PENDING', $3, $4)
       RETURNING *`,
      [p.id, amount_cents, payment_method, payment_details]
    );

    return res.json({ success: true, withdrawal: result.rows[0], message: 'Withdrawal request submitted. Admin will review and process your payment.' });
  } catch (err) {
    console.error('[PARTNER WITHDRAWAL ERROR]', err);
    return res.status(500).json({ success: false, error: 'WITHDRAWAL_ERROR', message: err.message });
  }
});

// GET /api/v1/partner/withdrawals?key=...
router.get('/withdrawals', requirePartnerKey, async (req, res) => {
  try {
    const result = await db.query(
      `SELECT id, amount_cents, status, payment_method, created_at, reviewed_at, paid_at, admin_notes
       FROM withdrawal_requests
       WHERE partnership_id = $1
       ORDER BY created_at DESC
       LIMIT 100`,
      [req.partner.id]
    );
    return res.json({ success: true, withdrawals: result.rows });
  } catch (err) {
    console.error('[PARTNER WITHDRAWALS LIST ERROR]', err);
    return res.status(500).json({ success: false, error: 'LIST_ERROR', message: err.message });
  }
});

// Mask email for privacy: lok***@gmail.com
function maskEmail(email) {
  if (!email) return '***@***.com';
  const [local, domain] = email.split('@');
  if (local.length <= 3) return `${local[0]}***@${domain}`;
  return `${local.slice(0, 3)}***@${domain}`;
}

module.exports = router;
