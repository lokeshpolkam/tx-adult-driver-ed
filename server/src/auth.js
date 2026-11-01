const jwt = require('jsonwebtoken');
const { OAuth2Client } = require('google-auth-library');

const JWT_SECRET = (process.env.JWT_SECRET || 'dev_jwt_secret_tx_ade_secure_key_1234567890').trim();
const GOOGLE_CLIENT_ID = (process.env.GOOGLE_CLIENT_ID && process.env.GOOGLE_CLIENT_ID !== 'PLACEHOLDER'
  ? process.env.GOOGLE_CLIENT_ID
  : '1004296326114-dq4t23m4evubp6jv6jovjd955ju808jc.apps.googleusercontent.com').trim();

const googleClient = new OAuth2Client(GOOGLE_CLIENT_ID);

async function verifyGoogleIdToken(idToken) {
  if (!idToken) throw new Error('ID token is required');

  // Cryptographically verify the Google ID token signature against Google's public certs
  const ticket = await googleClient.verifyIdToken({
    idToken,
    audience: GOOGLE_CLIENT_ID,
  });
  const payload = ticket.getPayload();
  if (!payload || !payload.email_verified) {
    throw new Error('Google email is not verified');
  }

  return {
    google_sub: payload.sub,
    email: payload.email.toLowerCase(),
    name: payload.name || payload.email.split('@')[0],
    picture: payload.picture || null,
    email_verified: payload.email_verified,
  };
}

function mintSessionJwt(user) {
  return jwt.sign(
    {
      id: user.id,
      email: user.email,
      role: user.role || 'STUDENT',
      enrollment_status: user.enrollment_status || 'UNPAID',
    },
    JWT_SECRET,
    { expiresIn: '7d' }
  );
}

function verifySessionJwt(token) {
  return jwt.verify(token, JWT_SECRET);
}

function requireAuth(req, res, next) {
  let token = req.cookies?.tx_session;
  if (!token && req.headers.authorization?.startsWith('Bearer ')) {
    token = req.headers.authorization.split(' ')[1];
  }

  if (!token) {
    return res.status(401).json({ success: false, error: 'UNAUTHORIZED', message: 'Authentication required' });
  }

  try {
    const payload = verifySessionJwt(token);
    req.user = payload;
    next();
  } catch (err) {
    return res.status(401).json({ success: false, error: 'INVALID_SESSION', message: 'Session expired or invalid' });
  }
}

function optionalAuth(req, res, next) {
  let token = req.cookies?.tx_session;
  if (!token && req.headers.authorization?.startsWith('Bearer ')) {
    token = req.headers.authorization.split(' ')[1];
  }

  if (token) {
    try {
      const payload = verifySessionJwt(token);
      req.user = payload;
    } catch (_) {}
  }
  next();
}

const db = require('./db');

async function requireActiveEnrollment(req, res, next) {
  if (!req.user) {
    return res.status(401).json({ success: false, error: 'UNAUTHORIZED' });
  }

  // Allow Module 1 for unpaid users as a free trial preview
  const topicId = req.body?.topicId || req.query?.topicId || '';
  if (topicId && topicId.startsWith('L01-')) {
    return next();
  }

  // Check in-memory JWT status first
  if (req.user.enrollment_status === 'ACTIVE') {
    return next();
  }

  // Authoritative check against Cloud SQL database
  try {
    const userRes = await db.query('SELECT enrollment_status FROM users WHERE id = $1', [req.user.id]);
    if (userRes.rows[0]?.enrollment_status === 'ACTIVE') {
      req.user.enrollment_status = 'ACTIVE';
      return next();
    }
  } catch (err) {
    console.error('[AUTH DB CHECK ERROR]', err);
  }

  return res.status(403).json({
    success: false,
    error: 'PAYMENT_REQUIRED',
    message: 'Active course enrollment required to access Modules 2 through 9. Please complete enrollment.'
  });
}

module.exports = {
  verifyGoogleIdToken,
  mintSessionJwt,
  verifySessionJwt,
  requireAuth,
  optionalAuth,
  requireActiveEnrollment,
};
