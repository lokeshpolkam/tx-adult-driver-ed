const express = require('express');
const router = express.Router();
const crypto = require('crypto');
const db = require('../db');
const { getRedis } = require('../redis');
const { requireAuth, requireActiveEnrollment } = require('../auth');

const ALL_TOPIC_IDS = [
  'L01-T01', 'L01-T02', 'L01-T03',
  'L02-T01', 'L02-T02', 'L02-T03', 'L02-T04', 'L02-T05', 'L02-T06', 'L02-T07',
  'L03-T01', 'L03-T02', 'L03-T03', 'L03-T04', 'L03-T05', 'L03-T06', 'L03-T07',
  'L04-T01', 'L04-T02', 'L04-T03', 'L04-T04',
  'L05-T01', 'L05-T02', 'L05-T03', 'L05-T04', 'L05-T05', 'L05-T06', 'L05-T07', 'L05-T08', 'L05-T09', 'L05-T10', 'L05-T11', 'L05-T12', 'L05-T13', 'L05-T14', 'L05-T15', 'L05-T16', 'L05-T17', 'L05-T18',
  'L06-T01', 'L06-T02', 'L06-T03', 'L06-T04', 'L06-T05', 'L06-T06', 'L06-T07',
  'L07-T01', 'L07-T02', 'L07-T03', 'L07-T04', 'L07-T05', 'L07-T06', 'L07-T07', 'L07-T08', 'L07-T09', 'L07-T10', 'L07-T11', 'L07-T12', 'L07-T13', 'L07-T14', 'L07-T15', 'L07-T16', 'L07-T17', 'L07-T18',
  'L08-T01', 'L08-T02', 'L08-T03', 'L08-T04', 'L08-T05', 'L08-T06', 'L08-T07', 'L08-T08', 'L08-T09', 'L08-T10',
  'L09-T01', 'L09-T02'
];

function hashAnswer(answer) {
  const normalized = answer.trim().toLowerCase().replace(/[^a-z0-9]/g, '');
  return crypto.createHash('sha256').update(normalized).digest('hex');
}

// GET /api/v1/student/progress
router.get('/progress', requireAuth, async (req, res) => {
  try {
    const userId = req.user.id;

    // Fetch user profile including last_active_topic
    const userRes = await db.query(
      `SELECT id, email, full_name, legal_first_name, legal_last_name, date_of_birth, dl_or_ssn_last4, role, enrollment_status, last_active_topic FROM users WHERE id = $1`,
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
    let totalInstructionalSeconds = 0;

    for (const t of topicsRes.rows) {
      totalInstructionalSeconds += (t.instructional_seconds || 0);
      if (t.status === 'COMPLETED') {
        completedTopics.push(t.topic_id);
      }
    }

    const completedSet = new Set(completedTopics);

    // 1. Next uncompleted topic strictly in sequential curriculum order
    const nextUncompleted = ALL_TOPIC_IDS.find(id => !completedSet.has(id)) || 'L01-T01';

    // 2. Determine last active topic where user stopped:
    let lastActiveTopic = user?.last_active_topic || 'L01-T01';
    if (!ALL_TOPIC_IDS.includes(lastActiveTopic)) {
      lastActiveTopic = nextUncompleted;
    }

    // 3. TDLR Progression Guard: A student cannot be placed on Module 9 (L09-T01 PVQ or L09-T02 Final Exam)
    // unless all 74 instructional topics in Modules 1 through 8 have been completed!
    const mod9Topics = ['L09-T01', 'L09-T02'];
    if (mod9Topics.includes(lastActiveTopic)) {
      const priorTopics = ALL_TOPIC_IDS.filter(id => !mod9Topics.includes(id));
      const allPriorCompleted = priorTopics.every(id => completedSet.has(id));
      if (!allPriorCompleted) {
        lastActiveTopic = nextUncompleted;
      }
    }

    const unlockedTopicId = lastActiveTopic;

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
        legalFirstName: user.legal_first_name,
        legalLastName: user.legal_last_name,
        dateOfBirth: user.date_of_birth,
        dlOrSsnLast4: user.dl_or_ssn_last4,
        enrollmentStatus: user.enrollment_status,
        pvqConfigured,
        completedTopics,
        completedTopicsCount: completedTopics.length,
        totalTopics: ALL_TOPIC_IDS.length,
        unlockedTopicId,
        lastActiveTopic,
        nextUncompletedTopicId: nextUncompleted,
        progressPercentage: Math.round((completedTopics.length / ALL_TOPIC_IDS.length) * 100),
        totalInstructionalSeconds,
        requiredSeconds: 21600, // 6 hours mandated by TDLR
        isCourseCompleted: completedTopics.length === ALL_TOPIC_IDS.length && totalInstructionalSeconds >= 21600,
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

// POST /api/v1/student/progress/complete
// Save topic completion to Cloud SQL
router.post('/progress/complete', requireAuth, async (req, res) => {
  try {
    const userId = req.user.id;
    const { topicId, nextTopicId, instructionalSeconds = 0 } = req.body;
    if (!topicId) {
      return res.status(400).json({ success: false, error: 'MISSING_TOPIC_ID' });
    }

    const moduleId = parseInt(topicId.substring(1, 3), 10) || 1;

    // Ensure student progress is never lost across devices
    const userRes = await db.query('SELECT enrollment_status, role FROM users WHERE id = $1', [userId]);
    const isEnrolled = userRes.rows[0]?.enrollment_status === 'ACTIVE' || userRes.rows[0]?.role === 'ADMIN';

    // TDLR Anti-Tampering (16 TAC § 84.500): Instructional time cannot be forged via bulk integers in progress completion.
    // Instructional seconds are accumulated strictly via verified 30s server heartbeats.
    await db.query(
      `INSERT INTO topic_progress (user_id, topic_id, module_id, status, completed_at, updated_at)
       VALUES ($1, $2, $3, 'COMPLETED', NOW(), NOW())
       ON CONFLICT (user_id, topic_id) DO UPDATE
       SET status = 'COMPLETED',
           completed_at = COALESCE(topic_progress.completed_at, NOW()),
           updated_at = NOW()`,
      [userId, topicId, moduleId]
    );

    // Auto-resolve next topic if not explicitly sent
    let targetNextTopicId = nextTopicId;
    if (!targetNextTopicId) {
      const curIndex = ALL_TOPIC_IDS.indexOf(topicId);
      if (curIndex >= 0 && curIndex < ALL_TOPIC_IDS.length - 1) {
        targetNextTopicId = ALL_TOPIC_IDS[curIndex + 1];
      }
    }

    // Unlock next topic only if student is enrolled OR the next topic is still in Module 1
    if (targetNextTopicId) {
      const nextModuleId = parseInt(targetNextTopicId.substring(1, 3), 10) || 1;
      if (nextModuleId === 1 || isEnrolled) {
        await db.query(
          `INSERT INTO topic_progress (user_id, topic_id, module_id, status, unlocked_at, updated_at)
           VALUES ($1, $2, $3, 'UNLOCKED', NOW(), NOW())
           ON CONFLICT (user_id, topic_id) DO UPDATE
           SET status = CASE WHEN topic_progress.status = 'COMPLETED' THEN 'COMPLETED' ELSE 'UNLOCKED' END,
               updated_at = NOW()`,
          [userId, targetNextTopicId, nextModuleId]
        );
      }
    }

    const nextActive = targetNextTopicId || topicId;
    if (nextActive && ALL_TOPIC_IDS.includes(nextActive)) {
      db.query(`UPDATE users SET last_active_topic = $1, updated_at = NOW() WHERE id = $2`, [nextActive, userId])
        .catch(err => console.error('[UPDATE LAST ACTIVE TOPIC ERROR]', err.message));
    }

    return res.json({ success: true, message: `Topic ${topicId} marked as completed` });
  } catch (err) {
    console.error('[COMPLETE PROGRESS ERROR]', err);
    return res.status(500).json({ success: false, error: err.message });
  }
});

// POST /api/v1/student/progress/sync
// Authoritative server-driven progress sync: client synchronizes FROM server.
// Disallows arbitrary client-side bulk completion or timer forgery (TDLR 16 TAC §84.500 compliance)
router.post('/progress/sync', requireAuth, async (req, res) => {
  try {
    const userId = req.user.id;
    const { activeTopicId } = req.body;

    const userRes = await db.query('SELECT enrollment_status, role FROM users WHERE id = $1', [userId]);
    const isEnrolled = userRes.rows[0]?.enrollment_status === 'ACTIVE' || userRes.rows[0]?.role === 'ADMIN';

    // Update bookmark / active topic position if valid
    if (activeTopicId && ALL_TOPIC_IDS.includes(activeTopicId)) {
      db.query(`UPDATE users SET last_active_topic = $1, updated_at = NOW() WHERE id = $2`, [activeTopicId, userId])
        .catch(err => console.error('[UPDATE LAST ACTIVE TOPIC ERROR]', err.message));
      const activeModId = parseInt(activeTopicId.substring(1, 3), 10) || 1;
      if (activeModId === 1 || isEnrolled) {
        await db.query(
          `INSERT INTO topic_progress (user_id, topic_id, module_id, status, updated_at)
           VALUES ($1, $2, $3, 'IN_PROGRESS', NOW())
           ON CONFLICT (user_id, topic_id) DO UPDATE
           SET status = CASE WHEN topic_progress.status = 'COMPLETED' THEN 'COMPLETED' ELSE 'IN_PROGRESS' END,
               updated_at = NOW()`,
          [userId, activeTopicId, activeModId]
        );
      }
    }

    // Query authoritative database progress
    const progressRes = await db.query(
      `SELECT topic_id, status, instructional_seconds FROM topic_progress WHERE user_id = $1`,
      [userId]
    );

    const completed = [];
    let totalSeconds = 0;
    for (const r of progressRes.rows) {
      totalSeconds += (r.instructional_seconds || 0);
      if (r.status === 'COMPLETED') completed.push(r.topic_id);
    }

    return res.json({
      success: true,
      message: 'Authoritative server progress synchronized',
      completedTopics: completed,
      totalInstructionalSeconds: totalSeconds,
      activeTopicId: activeTopicId || 'L01-T01'
    });
  } catch (err) {
    console.error('[SYNC PROGRESS ERROR]', err);
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

    // Rate limiting check via Redis (with graceful in-memory tolerance)
    const redis = getRedis();
    const rateKey = `heartbeat:${userId}`;
    let lastPing = null;
    const now = Date.now();
    try {
      lastPing = await redis.get(rateKey);
    } catch (e) {
      console.warn('[REDIS] Heartbeat rate check warning:', e.message);
    }

    if (lastPing && (now - parseInt(lastPing, 10)) < 20000) {
      // Less than 20 seconds since last heartbeat -> reject
      return res.status(429).json({ success: false, error: 'RATE_LIMIT_EXCEEDED', message: 'Heartbeats must occur every 30 seconds' });
    }

    try {
      await redis.set(rateKey, String(now), 'EX', 300);
    } catch (e) {
      console.warn('[REDIS] Heartbeat rate set warning:', e.message);
    }

    // Get cumulative instructional time before adding delta
    const currentSumRes = await db.query(
      `SELECT SUM(instructional_seconds) as total FROM topic_progress WHERE user_id = $1`,
      [userId]
    );
    const currentTotal = parseInt(currentSumRes.rows[0].total || '0', 10);

    // STATUTORY MANDATE (16 TAC § 84.500): Exactly 6.00 clock hours (21,600s).
    // Timer stops counting at 21,600 seconds.
    if (currentTotal >= 21600) {
      return res.json({
        success: true,
        totalInstructionalSeconds: 21600,
        remainingSeconds: 0,
        timerCompleted: true,
        timerCapped: true,
        pvqDue: false,
        pvqChallenge: null,
      });
    }

    // Update student's last active topic in users table
    if (topicId && ALL_TOPIC_IDS.includes(topicId)) {
      db.query(`UPDATE users SET last_active_topic = $1, updated_at = NOW() WHERE id = $2`, [topicId, userId])
        .catch(err => console.error('[UPDATE LAST ACTIVE TOPIC ERROR]', err.message));
    }

    // Cap delta so cumulative time cannot exceed exactly 21,600 seconds
    const deltaToAdd = Math.min(validDelta, 21600 - currentTotal);

    // Increment topic instructional seconds in DB
    await db.query(
      `INSERT INTO topic_progress (user_id, topic_id, module_id, status, instructional_seconds, updated_at)
       VALUES ($1, $2, CAST(SUBSTRING($2 FROM 2 FOR 2) AS INTEGER), 'IN_PROGRESS', $3, NOW())
       ON CONFLICT (user_id, topic_id) DO UPDATE
       SET instructional_seconds = topic_progress.instructional_seconds + $3,
           status = CASE WHEN topic_progress.status = 'COMPLETED' THEN 'COMPLETED' ELSE 'IN_PROGRESS' END,
           updated_at = NOW()`,
      [userId, topicId, deltaToAdd]
    );

    // Insert audit log asynchronously (non-blocking write to protect heartbeat throughput at scale)
    const clientIp = req.headers['x-forwarded-for'] || req.socket.remoteAddress || '127.0.0.1';
    const userAgent = req.headers['user-agent'] || 'Unknown';
    db.query(
      `INSERT INTO instructional_time_logs (user_id, topic_id, delta_seconds, client_ip, user_agent)
       VALUES ($1, $2, $3, $4::inet, $5)`,
      [userId, topicId, deltaToAdd, clientIp.split(',')[0].trim(), userAgent]
    ).catch(err => console.error('[AUDIT LOG ERROR]', err.message));

    const finalTotal = Math.min(currentTotal + deltaToAdd, 21600);
    const isCompleted = (finalTotal >= 21600);

    // STRICT COMPLIANCE: ZERO in-lesson popup challenges during slide reading.
    // Personal Validation Questions (PVQ) are located strictly in Module 9 Topic 1 (L09-T01.html).
    return res.json({
      success: true,
      totalInstructionalSeconds: finalTotal,
      remainingSeconds: Math.max(21600 - finalTotal, 0),
      timerCompleted: isCompleted,
      timerCapped: isCompleted,
      pvqDue: false,
      pvqChallenge: null,
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

// PUT /api/v1/student/profile
// Authoritative Legal Identity & Verification Update for Form ADE-1317 (16 TAC § 84.500)
router.put('/profile', requireAuth, async (req, res) => {
  try {
    const userId = req.user.id;
    const { fullName, legalFirstName, legalLastName, dateOfBirth, dlOrSsnLast4 } = req.body;

    let dob = null;
    if (dateOfBirth) {
      const parsedDob = new Date(dateOfBirth);
      if (isNaN(parsedDob.getTime())) {
        return res.status(400).json({ success: false, error: 'INVALID_DOB', message: 'Valid date of birth is required.' });
      }
      // Verify adult driving age requirement (>= 18 years)
      const ageDiffMs = Date.now() - parsedDob.getTime();
      const ageDate = new Date(ageDiffMs);
      const age = Math.abs(ageDate.getUTCFullYear() - 1970);
      if (age < 18) {
        return res.status(400).json({ success: false, error: 'UNDERAGE', message: 'Texas Adult Driver Education is restricted to adults aged 18 and older.' });
      }
      dob = parsedDob.toISOString().split('T')[0];
    }

    let cleanLast4 = null;
    if (dlOrSsnLast4) {
      cleanLast4 = String(dlOrSsnLast4).trim().replace(/[^a-zA-Z0-9]/g, '').substring(0, 4);
      if (cleanLast4.length !== 4) {
        return res.status(400).json({ success: false, error: 'INVALID_IDENTIFIER', message: 'Last 4 digits of SSN or Driver License must be exactly 4 characters.' });
      }
    }

    const cleanFullName = fullName ? String(fullName).trim() : null;

    const updateRes = await db.query(
      `UPDATE users
       SET full_name = COALESCE($2, full_name),
           legal_first_name = COALESCE($3, legal_first_name),
           legal_last_name = COALESCE($4, legal_last_name),
           date_of_birth = COALESCE($5, date_of_birth),
           dl_or_ssn_last4 = COALESCE($6, dl_or_ssn_last4),
           updated_at = NOW()
       WHERE id = $1
       RETURNING id, email, full_name, legal_first_name, legal_last_name, date_of_birth, dl_or_ssn_last4, role, enrollment_status`,
      [userId, cleanFullName, legalFirstName, legalLastName, dob, cleanLast4]
    );

    return res.json({
      success: true,
      user: updateRes.rows[0],
      message: 'Student legal identity verified and saved for official state certificate Form ADE-1317.'
    });
  } catch (err) {
    console.error('[PROFILE UPDATE ERROR]', err);
    return res.status(500).json({ success: false, error: err.message });
  }
});

module.exports = router;

