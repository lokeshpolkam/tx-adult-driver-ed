const express = require('express');
const router = express.Router();
const crypto = require('crypto');
const db = require('../db');
const { getRedis } = require('../redis');
const { requireAuth, requireActiveEnrollment } = require('../auth');

function hashAnswer(answer) {
  const normalized = answer.trim().toLowerCase().replace(/[^a-z0-9]/g, '');
  return crypto.createHash('sha256').update(normalized).digest('hex');
}

// GET /api/v1/student/progress
router.get('/progress', requireAuth, async (req, res) => {
  try {
    const userId = req.user.id;

    // Fetch user profile
    const userRes = await db.query(
      `SELECT id, email, full_name, role, enrollment_status FROM users WHERE id = $1`,
      [userId]
    );
    const user = userRes.rows[0];

    // Fetch completed topics and instructional time
    const topicsRes = await db.query(
      `SELECT topic_id, module_id, status, instructional_seconds, completed_at
       FROM topic_progress
       WHERE user_id = $1
       ORDER BY topic_id ASC`,
      [userId]
    );

    const completedTopics = [];
    let unlockedTopicId = 'L01-T01';
    let totalInstructionalSeconds = 0;

    for (const t of topicsRes.rows) {
      totalInstructionalSeconds += t.instructional_seconds;
      if (t.status === 'COMPLETED') {
        completedTopics.push(t.topic_id);
      } else if (t.status === 'UNLOCKED' || t.status === 'IN_PROGRESS') {
        unlockedTopicId = t.topic_id;
      }
    }

    // Check PVQ setup
    const pvqRes = await db.query(
      `SELECT COUNT(*) as count FROM pvq_answers WHERE user_id = $1`,
      [userId]
    );
    const pvqConfigured = parseInt(pvqRes.rows[0].count, 10) >= 5;

    // Check certificate
    const certRes = await db.query(
      `SELECT serial_number, issued_at, verification_url FROM certificates WHERE user_id = $1`,
      [userId]
    );
    const certificate = certRes.rows[0] || null;

    return res.json({
      success: true,
      data: {
        userId: user.id,
        email: user.email,
        fullName: user.full_name,
        enrollmentStatus: user.enrollment_status,
        pvqConfigured,
        completedTopics,
        completedTopicsCount: completedTopics.length,
        totalTopics: 75,
        unlockedTopicId,
        progressPercentage: Math.round((completedTopics.length / 75) * 100),
        totalInstructionalSeconds,
        requiredSeconds: 21600, // 6 hours mandated by TDLR
        isCourseCompleted: completedTopics.length === 75 && totalInstructionalSeconds >= 21600,
        certificate: certificate ? {
          serialNumber: certificate.serial_number,
          issuedAt: certificate.issued_at,
          verificationUrl: certificate.verification_url,
        } : null,
      },
    });
  } catch (err) {
    console.error('[PROGRESS ERROR]', err);
    return res.status(500).json({ success: false, error: err.message });
  }
});

// POST /api/v1/student/heartbeat
// Mandated 30-second instructional timer enforcer (TDLR 16 TAC §84.500)
router.post('/heartbeat', requireAuth, requireActiveEnrollment, async (req, res) => {
  try {
    const userId = req.user.id;
    const { topicId, deltaSeconds = 30 } = req.body;

    if (!topicId) {
      return res.status(400).json({ success: false, error: 'MISSING_TOPIC_ID' });
    }

    // TDLR Anti-Tampering: Clamping delta to max 30s
    const validDelta = Math.min(Math.max(parseInt(deltaSeconds, 10), 0), 30);
    if (validDelta < 15) {
      return res.status(400).json({ success: false, error: 'DELTA_TOO_SMALL', message: 'Heartbeat interval too small' });
    }

    // Rate limiting check via Redis
    const redis = getRedis();
    const rateKey = `heartbeat:${userId}`;
    const lastPing = await redis.get(rateKey);
    const now = Date.now();

    if (lastPing && (now - parseInt(lastPing, 10)) < 20000) {
      // Less than 20 seconds since last heartbeat -> reject
      return res.status(429).json({ success: false, error: 'RATE_LIMIT_EXCEEDED', message: 'Heartbeats must occur every 30 seconds' });
    }

    await redis.set(rateKey, String(now), 'EX', 300);

    // Increment topic instructional seconds in DB
    await db.query(
      `INSERT INTO topic_progress (user_id, topic_id, module_id, status, instructional_seconds, updated_at)
       VALUES ($1, $2, CAST(SUBSTRING($2 FROM 2 FOR 2) AS INTEGER), 'IN_PROGRESS', $3, NOW())
       ON CONFLICT (user_id, topic_id) DO UPDATE
       SET instructional_seconds = topic_progress.instructional_seconds + $3,
           status = CASE WHEN topic_progress.status = 'COMPLETED' THEN 'COMPLETED' ELSE 'IN_PROGRESS' END,
           updated_at = NOW()`,
      [userId, topicId, validDelta]
    );

    // Insert audit log
    const clientIp = req.headers['x-forwarded-for'] || req.socket.remoteAddress || '127.0.0.1';
    const userAgent = req.headers['user-agent'] || 'Unknown';
    await db.query(
      `INSERT INTO instructional_time_logs (user_id, topic_id, delta_seconds, client_ip, user_agent)
       VALUES ($1, $2, $3, $4::inet, $5)`,
      [userId, topicId, validDelta, clientIp.split(',')[0].trim(), userAgent]
    );

    // Get cumulative instructional time
    const sumRes = await db.query(
      `SELECT SUM(instructional_seconds) as total FROM topic_progress WHERE user_id = $1`,
      [userId]
    );
    const totalSeconds = parseInt(sumRes.rows[0].total || '0', 10);

    // Check if PVQ challenge should be triggered (every ~3600 seconds or randomly)
    let pvqDue = false;
    let pvqChallenge = null;
    const pvqKey = `pvq_last:${userId}`;
    const lastPvqTime = await redis.get(pvqKey);

    if (!lastPvqTime || (now - parseInt(lastPvqTime, 10)) > 45 * 60 * 1000) {
      // Pick a random PVQ from user's configured answers
      const pvqQRes = await db.query(
        `SELECT question_key, question_prompt FROM pvq_answers WHERE user_id = $1 ORDER BY RANDOM() LIMIT 1`,
        [userId]
      );
      if (pvqQRes.rows.length > 0) {
        pvqDue = true;
        const q = pvqQRes.rows[0];
        pvqChallenge = {
          questionKey: q.question_key,
          questionPrompt: q.question_prompt,
          timeoutSeconds: 90, // Statutory 90s countdown
        };
        // Record presented challenge
        await db.query(
          `INSERT INTO pvq_challenges (user_id, question_key, presented_at)
           VALUES ($1, $2, NOW())`,
          [userId, q.question_key]
        );
        await redis.set(pvqKey, String(now), 'EX', 3600);
      }
    }

    return res.json({
      success: true,
      totalInstructionalSeconds: totalSeconds,
      remainingSeconds: Math.max(21600 - totalSeconds, 0),
      pvqDue,
      pvqChallenge,
    });
  } catch (err) {
    console.error('[HEARTBEAT ERROR]', err);
    return res.status(500).json({ success: false, error: err.message });
  }
});

// POST /api/v1/onboarding/pvq
// Record 5 Personal Validation Questions
router.post('/onboarding/pvq', requireAuth, async (req, res) => {
  try {
    const userId = req.user.id;
    const { answers, legalFirstName, legalLastName, dateOfBirth, dlOrSsnLast4 } = req.body;

    if (!Array.isArray(answers) || answers.length < 5) {
      return res.status(400).json({ success: false, error: 'INVALID_PVQ', message: 'At least 5 personal validation questions required' });
    }

    // Update user legal info if provided
    if (legalFirstName || legalLastName || dateOfBirth || dlOrSsnLast4) {
      await db.query(
        `UPDATE users
         SET legal_first_name = COALESCE($2, legal_first_name),
             legal_last_name = COALESCE($3, legal_last_name),
             date_of_birth = COALESCE($4, date_of_birth),
             dl_or_ssn_last4 = COALESCE($5, dl_or_ssn_last4),
             updated_at = NOW()
         WHERE id = $1`,
        [userId, legalFirstName, legalLastName, dateOfBirth, dlOrSsnLast4]
      );
    }

    // Insert hashed PVQ answers
    for (const item of answers) {
      const hashed = hashAnswer(item.answer);
      await db.query(
        `INSERT INTO pvq_answers (user_id, question_key, question_prompt, answer_hash)
         VALUES ($1, $2, $3, $4)
         ON CONFLICT (user_id, question_key) DO UPDATE
         SET answer_hash = EXCLUDED.answer_hash, question_prompt = EXCLUDED.question_prompt`,
        [userId, item.question_key, item.question_prompt, hashed]
      );
    }

    return res.json({ success: true, message: 'Personal validation questions registered successfully' });
  } catch (err) {
    console.error('[PVQ SETUP ERROR]', err);
    return res.status(500).json({ success: false, error: err.message });
  }
});

// POST /api/v1/pvq/verify
// Verify challenge response within 90-second limit
router.post('/pvq/verify', requireAuth, async (req, res) => {
  try {
    const userId = req.user.id;
    const { questionKey, answer } = req.body;

    if (!questionKey || !answer) {
      return res.status(400).json({ success: false, error: 'MISSING_DATA' });
    }

    const hashedAttempt = hashAnswer(answer);

    const record = await db.query(
      `SELECT answer_hash FROM pvq_answers WHERE user_id = $1 AND question_key = $2`,
      [userId, questionKey]
    );

    if (record.rows.length === 0) {
      return res.status(404).json({ success: false, error: 'QUESTION_NOT_FOUND' });
    }

    const isCorrect = record.rows[0].answer_hash === hashedAttempt;

    // Update challenge record
    await db.query(
      `UPDATE pvq_challenges
       SET answered_at = NOW(),
           is_correct = $3
       WHERE user_id = $1 AND question_key = $2 AND answered_at IS NULL`,
      [userId, questionKey, isCorrect]
    );

    return res.json({
      success: true,
      isCorrect,
      message: isCorrect ? 'Identity verified successfully' : 'Incorrect answer',
    });
  } catch (err) {
    return res.status(500).json({ success: false, error: err.message });
  }
});

module.exports = router;
