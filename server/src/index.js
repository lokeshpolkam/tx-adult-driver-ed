require('dotenv').config();
const express = require('express');
const cors = require('cors');
const cookieParser = require('cookie-parser');
const db = require('./db');

const authRoutes = require('./routes/auth');
const billingRoutes = require('./routes/billing');
const studentRoutes = require('./routes/student');
const lessonsRoutes = require('./routes/lessons');
const quizzesRoutes = require('./routes/quizzes');
const certificatesRoutes = require('./routes/certificates');

const app = express();
const PORT = process.env.PORT || 8080;

// Trust Cloud Run / Cloud Load Balancer reverse proxies
app.set('trust proxy', true);

// CORS configuration
const allowedOrigins = [
  'http://localhost:3000',
  'http://localhost:8080',
  'http://127.0.0.1:3000',
  'http://127.0.0.1:8080',
  'https://app.texasade.org',
  'https://texasade.org',
  'https://courseshell.vercel.app',
];

const isOriginAllowed = (origin) => {
  if (!origin) return true;
  if (allowedOrigins.includes(origin)) return true;
  if (origin.endsWith('.vercel.app')) return true;
  if (process.env.NODE_ENV !== 'production') return true;
  return false;
};

app.use(
  cors({
    origin: (origin, callback) => {
      if (isOriginAllowed(origin)) {
        callback(null, true);
      } else {
        callback(null, false);
      }
    },
    credentials: true,
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With'],
  })
);

// Note: Stripe webhook uses raw body, so mount it before global express.json()
app.use('/api/v1/billing/webhook', express.raw({ type: 'application/json' }), (req, res, next) => {
  // Pass through to billing router
  next();
});

// Parsers
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());

// Security Headers
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  next();
});

// API Routes
app.use('/api/v1/auth', authRoutes);
app.use('/api/v1/billing', billingRoutes);
app.use('/api/v1/student', studentRoutes);
app.use('/api/v1', lessonsRoutes);
app.use('/api/v1', quizzesRoutes);
app.use('/api/v1/certificates', certificatesRoutes);
app.use('/api/v1/public', certificatesRoutes);

// Health Endpoint
app.get('/api/v1/health', async (req, res) => {
  let dbStatus = 'UNKNOWN';
  try {
    await db.query('SELECT 1');
    dbStatus = 'CONNECTED';
  } catch (err) {
    dbStatus = `DISCONNECTED: ${err.message}`;
  }

  return res.json({
    status: 'HEALTHY',
    service: 'Texas Adult Driver Education Unified API',
    courseApproval: 'TDLR Course ADE-1317 (16 TAC §84.500)',
    workZoneMandate: 'Compliant with HB 1884 / TTC §472.022 (Sept 1, 2026)',
    database: dbStatus,
    timestamp: new Date().toISOString(),
  });
});

// Global Error Handler
app.use((err, req, res, next) => {
  console.error('[UNHANDLED ERROR]', err);
  return res.status(500).json({
    success: false,
    error: 'INTERNAL_ERROR',
    message: process.env.NODE_ENV === 'production' ? 'An internal error occurred' : err.message,
  });
});

// Start Server
app.listen(PORT, () => {
  console.log(`[SERVER] TX-ADE Unified API listening on port ${PORT}`);
  console.log(`[SERVER] Environment: ${process.env.NODE_ENV || 'development'}`);
});
