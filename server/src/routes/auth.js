const express = require('express');
const router = express.Router();
const db = require('../db');
const bcrypt = require('bcrypt');
const { verifyGoogleIdToken, mintSessionJwt, requireAuth } = require('../auth');
const { sendWelcomeEmail } = require('../email');

const PRIMARY_ADMIN_EMAIL = (process.env.PRIMARY_ADMIN_EMAIL || 'admin@texasade.org').toLowerCase().trim();

// POST /api/v1/auth/register
router.post('/register', async (req, res) => {
  try {
    const { email, password, fullName, dateOfBirth } = req.body;
    if (!email || !password || !fullName || !dateOfBirth) {
      return res.status(400).json({ success: false, error: 'MISSING_FIELDS', message: 'All fields are required.' });
    }

    const cleanEmail = email.trim().toLowerCase();
    
    // Check if user already exists
    const existing = await db.query('SELECT id FROM users WHERE email = $1', [cleanEmail]);
    if (existing.rows.length > 0) {
      return res.status(409).json({ success: false, error: 'USER_EXISTS', message: 'An account with this email already exists.' });
    }

    // Hash password
    const saltRounds = 12;
    const passwordHash = await bcrypt.hash(password, saltRounds);

    const initialRole = (cleanEmail === PRIMARY_ADMIN_EMAIL) ? 'ADMIN' : 'STUDENT';

    // Insert user
    const insertSql = `
      INSERT INTO users (email, password_hash, full_name, date_of_birth, enrollment_status, role)
      VALUES ($1, $2, $3, $4, 'UNPAID', $5)
      RETURNING id, email, full_name, role, enrollment_status;
    `;
    const result = await db.query(insertSql, [cleanEmail, passwordHash, fullName, dateOfBirth, initialRole]);
    const user = result.rows[0];

    const sessionToken = mintSessionJwt(user);
    
    // Set cookie
    const isProduction = process.env.NODE_ENV === 'production';
    res.cookie('tx_session', sessionToken, {
      httpOnly: true,
      secure: isProduction,
      sameSite: isProduction ? 'None' : 'Lax',
      maxAge: 7 * 24 * 60 * 60 * 1000, // 7 days
      path: '/',
    });

    // Dispatch clean welcome email asynchronously
    sendWelcomeEmail({ email: user.email, fullName: user.full_name }).catch((e) =>
      console.warn('[EMAIL] Welcome email failed on /register:', e.message)
    );

    return res.json({
      success: true,
      token: sessionToken,
      user: {
        id: user.id,
        email: user.email,
        fullName: user.full_name,
        role: user.role || 'STUDENT',
        enrollmentStatus: user.enrollment_status,
      },
    });
  } catch (err) {
    console.error('[REGISTER ERROR]', err);
    return res.status(500).json({ success: false, error: 'REGISTER_FAILED', message: 'Internal server error.' });
  }
});

// POST /api/v1/auth/login
router.post('/login', async (req, res) => {
  try {
    const { email, password, rememberMe } = req.body;
    if (!email || !password) {
      return res.status(400).json({ success: false, error: 'MISSING_CREDENTIALS', message: 'Email and password are required.' });
    }

    const cleanEmail = email.trim().toLowerCase();
    const result = await db.query('SELECT * FROM users WHERE email = $1', [cleanEmail]);
    
    if (result.rows.length === 0) {
      return res.status(401).json({ success: false, error: 'INVALID_CREDENTIALS', message: 'Invalid email or password.' });
    }

    const user = result.rows[0];
    
    // Verify password if it exists
    if (!user.password_hash) {
      return res.status(401).json({ success: false, error: 'OAUTH_ONLY', message: 'Please sign in with Google or use the email link.' });
    }

    const match = await bcrypt.compare(password, user.password_hash);
    if (!match) {
      return res.status(401).json({ success: false, error: 'INVALID_CREDENTIALS', message: 'Invalid email or password.' });
    }

    if (user.email.toLowerCase() === PRIMARY_ADMIN_EMAIL && user.role !== 'ADMIN') {
      await db.query(`UPDATE users SET role = 'ADMIN' WHERE id = $1`, [user.id]);
      user.role = 'ADMIN';
    }

    const sessionToken = mintSessionJwt(user);
    const maxAge = rememberMe ? 30 * 24 * 60 * 60 * 1000 : 7 * 24 * 60 * 60 * 1000;
    
    const isProduction = process.env.NODE_ENV === 'production';
    res.cookie('tx_session', sessionToken, {
      httpOnly: true,
      secure: isProduction,
      sameSite: isProduction ? 'None' : 'Lax',
      maxAge: maxAge,
      path: '/',
    });

    return res.json({
      success: true,
      token: sessionToken,
      user: {
        id: user.id,
        email: user.email,
        fullName: user.full_name,
        role: user.role || 'STUDENT',
        enrollmentStatus: user.enrollment_status,
        profileImage: user.profile_image,
      },
    });
  } catch (err) {
    console.error('[LOGIN ERROR]', err);
    return res.status(500).json({ success: false, error: 'LOGIN_FAILED', message: 'Internal server error.' });
  }
});

// POST /api/v1/auth/google
router.post('/google', async (req, res) => {
  try {
    const { id_token } = req.body;
    if (!id_token) {
      return res.status(400).json({ success: false, error: 'MISSING_TOKEN', message: 'Google id_token is required' });
    }

    const googleUser = await verifyGoogleIdToken(id_token);

    // Authoritative Account Linking: Resolve users_email_key duplicate conflict
    const cleanEmail = googleUser.email.toLowerCase().trim();
    const existingRes = await db.query(
      `SELECT id, google_sub, email, full_name, legal_first_name, legal_last_name, role, enrollment_status, profile_image
       FROM users WHERE google_sub = $1 OR email = $2 LIMIT 1`,
      [googleUser.google_sub, cleanEmail]
    );

    let user;
    if (existingRes.rows.length > 0) {
      // User exists by email or previous SSO: Link google_sub and preserve user state
      const updateRes = await db.query(
        `UPDATE users
         SET google_sub = $1,
             full_name = CASE WHEN full_name IS NULL OR full_name = '' THEN $2 ELSE full_name END,
             profile_image = COALESCE($3, profile_image),
             updated_at = NOW()
         WHERE id = $4
         RETURNING id, google_sub, email, full_name, legal_first_name, legal_last_name, role, enrollment_status, profile_image`,
        [googleUser.google_sub, googleUser.name, googleUser.picture, existingRes.rows[0].id]
      );
      user = updateRes.rows[0];
      user.is_new_user = false;
    } else {
      // New student registration
      const insertRes = await db.query(
        `INSERT INTO users (google_sub, email, full_name, profile_image)
         VALUES ($1, $2, $3, $4)
         RETURNING id, google_sub, email, full_name, legal_first_name, legal_last_name, role, enrollment_status, profile_image`,
        [googleUser.google_sub, cleanEmail, googleUser.name, googleUser.picture]
      );
      user = insertRes.rows[0];
      user.is_new_user = true;
    }

    // Ensure primary admin email automatically gets ADMIN role
    const PRIMARY_ADMIN_EMAIL = (process.env.PRIMARY_ADMIN_EMAIL || 'admin@texasade.org').toLowerCase().trim();
    if (user.email.toLowerCase() === PRIMARY_ADMIN_EMAIL && user.role !== 'ADMIN') {
      await db.query(`UPDATE users SET role = 'ADMIN' WHERE id = $1`, [user.id]);
      user.role = 'ADMIN';
    }

    const sessionToken = mintSessionJwt(user);

    // If new student, dispatch clean welcome email
    if (user.is_new_user) {
      sendWelcomeEmail({ email: user.email, fullName: user.full_name }).catch((e) =>
        console.warn('[EMAIL] Welcome email failed on Google signup:', e.message)
      );
    }

    // Set secure HTTP-only cookie
    const isProduction = process.env.NODE_ENV === 'production';
    res.cookie('tx_session', sessionToken, {
      httpOnly: true,
      secure: isProduction,
      sameSite: isProduction ? 'None' : 'Lax',
      maxAge: 7 * 24 * 60 * 60 * 1000, // 7 days
      path: '/',
    });

    return res.json({
      success: true,
      token: sessionToken,
      user: {
        id: user.id,
        email: user.email,
        fullName: user.full_name,
        role: user.role || 'STUDENT',
        enrollmentStatus: user.enrollment_status,
        profileImage: user.profile_image,
      },
    });
  } catch (err) {
    console.error('[AUTH ERROR]', err);
    return res.status(401).json({ success: false, error: 'AUTH_FAILED', message: err.message });
  }
});

// POST /api/v1/auth/email
// Universal student email authentication (Yahoo, Outlook, iCloud, Gmail, etc.)
router.post('/email', async (req, res) => {
  try {
    const { email, fullName = '', promoCode = '' } = req.body;
    if (!email || !email.includes('@')) {
      return res.status(400).json({ success: false, error: 'INVALID_EMAIL', message: 'A valid student email address is required' });
    }

    const cleanEmail = email.trim().toLowerCase();
    const cleanName = (fullName || cleanEmail.split('@')[0]).trim();
    const cleanPromo = (promoCode || '').trim().toUpperCase();

    const adminSecret = req.headers['x-admin-secret'] || req.body?.adminSecret;
    const isAuthorizedAdmin = (adminSecret && adminSecret === process.env.ADMIN_SECRET);
    const isWaiver = isAuthorizedAdmin && ['TEXASVIP', 'TDLRADMIN'].includes(cleanPromo);
    const initialStatus = isWaiver ? 'ACTIVE' : 'UNPAID';
    const emailSub = `email_${cleanEmail}`;

    const upsertSql = `
      INSERT INTO users (google_sub, email, full_name, enrollment_status)
      VALUES ($1, $2, $3, $4)
      ON CONFLICT (email) DO UPDATE
      SET full_name = CASE WHEN users.full_name IS NULL OR users.full_name = '' THEN EXCLUDED.full_name ELSE users.full_name END,
          enrollment_status = CASE WHEN EXCLUDED.enrollment_status = 'ACTIVE' THEN 'ACTIVE' ELSE users.enrollment_status END,
          updated_at = NOW()
      RETURNING id, google_sub, email, full_name, legal_first_name, legal_last_name, role, enrollment_status, profile_image;
    `;
    const result = await db.query(upsertSql, [
      emailSub,
      cleanEmail,
      cleanName,
      initialStatus,
    ]);

    const user = result.rows[0];

    // If waiver code used by authorized admin, grant active enrollment
    if (isWaiver) {
      const simSessionId = `waiver_${cleanPromo.toLowerCase() || 'code'}_${user.id}_${Date.now()}`;
      await db.query(
        `INSERT INTO enrollments (user_id, stripe_session_id, tier, amount_cents, status, paid_at, expires_at)
         VALUES ($1, $2, 'STANDARD', 0, 'ACTIVE', NOW(), NOW() + INTERVAL '90 days')
         ON CONFLICT (stripe_session_id) DO NOTHING`,
        [user.id, simSessionId]
      );
      await db.query(
        `INSERT INTO topic_progress (user_id, topic_id, module_id, status, unlocked_at)
         VALUES ($1, 'L01-T01', 1, 'UNLOCKED', NOW())
         ON CONFLICT (user_id, topic_id) DO NOTHING`,
        [user.id]
      );
    }

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
        role: user.role || 'STUDENT',
        enrollmentStatus: user.enrollment_status,
        profileImage: user.profile_image,
      },
    });
  } catch (err) {
    console.error('[EMAIL AUTH ERROR]', err);
    return res.status(500).json({ success: false, error: 'AUTH_FAILED', message: err.message });
  }
});

// GET /api/v1/auth/me
router.get('/me', requireAuth, async (req, res) => {
  try {
    const userRes = await db.query(
      `SELECT id, email, full_name, legal_first_name, legal_last_name, role, enrollment_status, profile_image, created_at FROM users WHERE id = $1`,
      [req.user.id]
    );

    if (userRes.rows.length === 0) {
      return res.status(404).json({ success: false, error: 'USER_NOT_FOUND' });
    }

    let user = userRes.rows[0];
    const PRIMARY_ADMIN_EMAIL = (process.env.PRIMARY_ADMIN_EMAIL || 'admin@texasade.org').toLowerCase().trim();
    if (user.email && user.email.toLowerCase() === PRIMARY_ADMIN_EMAIL && user.role !== 'ADMIN') {
      await db.query(`UPDATE users SET role = 'ADMIN' WHERE id = $1`, [user.id]);
      user.role = 'ADMIN';
    }

    return res.json({
      success: true,
      user: {
        ...user,
        role: user.role || 'STUDENT',
        fullName: user.full_name,
        enrollmentStatus: user.enrollment_status,
      }
    });
  } catch (err) {
    return res.status(500).json({ success: false, error: err.message });
  }
});

// POST or GET /api/v1/auth/logout
const handleLogoutRequest = (req, res) => {
  res.cookie('tx_session', '', {
    path: '/',
    httpOnly: true,
    secure: true,
    sameSite: 'None',
    expires: new Date(0),
    maxAge: 0,
  });
  return res.json({ success: true, message: 'Logged out successfully' });
};

router.post('/logout', handleLogoutRequest);
router.get('/logout', handleLogoutRequest);

// GET /api/v1/auth/all-users
// List recent registered students in Cloud SQL
router.get('/all-users', async (req, res) => {
  try {
    const result = await db.query(
      `SELECT id, email, full_name, role, enrollment_status, created_at FROM users ORDER BY created_at DESC LIMIT 20`
    );
    return res.json({ success: true, count: result.rows.length, users: result.rows });
  } catch (err) {
    return res.status(500).json({ success: false, error: err.message });
  }
});

module.exports = router;
