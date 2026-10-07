const express = require('express');
const router = express.Router();
const db = require('../db');
const { verifyGoogleIdToken, mintSessionJwt, requireAuth } = require('../auth');

// POST /api/v1/auth/google
router.post('/google', async (req, res) => {
  try {
    const { id_token } = req.body;
    if (!id_token) {
      return res.status(400).json({ success: false, error: 'MISSING_TOKEN', message: 'Google id_token is required' });
    }

    const googleUser = await verifyGoogleIdToken(id_token);

    // Upsert user into database
    const upsertSql = `
      INSERT INTO users (google_sub, email, full_name, profile_image)
      VALUES ($1, $2, $3, $4)
      ON CONFLICT (google_sub) DO UPDATE
      SET full_name = EXCLUDED.full_name,
          profile_image = COALESCE(EXCLUDED.profile_image, users.profile_image),
          updated_at = NOW()
      RETURNING id, google_sub, email, full_name, legal_first_name, legal_last_name, role, enrollment_status, profile_image;
    `;
    const result = await db.query(upsertSql, [
      googleUser.google_sub,
      googleUser.email.toLowerCase(),
      googleUser.name,
      googleUser.picture,
    ]);

    const user = result.rows[0];
    const sessionToken = mintSessionJwt(user);

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
        enrollmentStatus: user.enrollment_status,
        profileImage: user.profile_image,
      },
    });
  } catch (err) {
    console.error('[AUTH ERROR]', err);
    return res.status(401).json({ success: false, error: 'AUTH_FAILED', message: err.message });
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

    return res.json({ success: true, user: userRes.rows[0] });
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
