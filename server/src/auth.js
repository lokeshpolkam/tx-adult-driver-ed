const jwt = require('jsonwebtoken');
const { OAuth2Client } = require('google-auth-library');

const JWT_SECRET = process.env.JWT_SECRET || 'dev_jwt_secret_tx_ade_secure_key_1234567890';
const GOOGLE_CLIENT_ID = (process.env.GOOGLE_CLIENT_ID || '').trim();

const googleClient = new OAuth2Client(GOOGLE_CLIENT_ID);

async function verifyGoogleIdToken(idToken) {
  if (!idToken) throw new Error('ID token is required');
  
  // If no valid GOOGLE_CLIENT_ID is set yet, allow mock or decoded JWT
  if (!GOOGLE_CLIENT_ID || GOOGLE_CLIENT_ID === 'PLACEHOLDER' || !GOOGLE_CLIENT_ID.includes('.apps.googleusercontent.com')) {
    const decoded = jwt.decode(idToken);
    if (decoded && decoded.email) {
      return {
        google_sub: decoded.sub || 'mock_sub_' + decoded.email,
        email: decoded.email,
        name: decoded.name || decoded.email.split('@')[0],
        picture: decoded.picture || null,
        email_verified: true,
      };
    }
  }

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
    email: payload.email,
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

function requireActiveEnrollment(req, res, next) {
  if (!req.user) {
    return res.status(401).json({ success: false, error: 'UNAUTHORIZED' });
  }

  // Allow Module 1 for unpaid users as a free trial preview
  const topicId = req.body?.topicId || req.query?.topicId || '';
  if (topicId && topicId.startsWith('L01-')) {
    return next();
  }

  if (req.user.enrollment_status !== 'ACTIVE') {
    return res.status(403).json({
      success: false,
      error: 'PAYMENT_REQUIRED',
      message: 'Active course enrollment required to access Modules 2 through 9. Use promo code TEXAS100 for 100% off.'
    });
  }
  next();
}

module.exports = {
  verifyGoogleIdToken,
  mintSessionJwt,
  verifySessionJwt,
  requireAuth,
  requireActiveEnrollment,
};
