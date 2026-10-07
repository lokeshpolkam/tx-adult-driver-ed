const express = require('express');
const router = express.Router();
const crypto = require('crypto');
const db = require('../db');
const { getRedis } = require('../redis');
const { getLessonHtml, getAsset } = require('../gcs');
const { requireAuth, requireActiveEnrollment } = require('../auth');
const { generateAntiTamperScript } = require('../anti_tamper');

const TICKET_SECRET = process.env.TICKET_SECRET || 'dev_ticket_secret_tx_ade_secure_key_1234567890';

// Module end topics mapping
const MODULE_END_TOPICS = {
  'L01-T03': 1,
  'L02-T07': 2,
  'L03-T07': 3,
  'L04-T04': 4,
  'L05-T18': 5,
  'L06-T07': 6,
  'L07-T18': 7,
  'L08-T10': 8,
  'L09-T01': 9, // Final exam
};

// Next topic mapping (linear curriculum)
function getNextTopicId(topicId) {
  const mod = parseInt(topicId.slice(1, 3), 10);
  const top = parseInt(topicId.slice(4, 6), 10);

  const moduleMax = { 1: 3, 2: 7, 3: 7, 4: 4, 5: 18, 6: 7, 7: 18, 8: 10, 9: 1 };

  if (top < moduleMax[mod]) {
    const nextTop = String(top + 1).padStart(2, '0');
    return `L${String(mod).padStart(2, '0')}-T${nextTop}`;
  } else if (mod < 9) {
    const nextMod = String(mod + 1).padStart(2, '0');
    return `L${nextMod}-T01`;
  }
  return null;
}

// POST /api/v1/lessons/:topicId/ticket
// Request single-use ephemeral ticket to load iframe
router.post('/lessons/:topicId/ticket', requireAuth, requireActiveEnrollment, async (req, res) => {
  try {
    const userId = req.user.id;
    const topicId = req.params.topicId.toUpperCase();

    // Verify topic is UNLOCKED or COMPLETED for this student
    const progressRes = await db.query(
      `SELECT status FROM topic_progress WHERE user_id = $1 AND topic_id = $2`,
      [userId, topicId]
    );

    const status = progressRes.rows[0]?.status;
    if (!status || (status !== 'UNLOCKED' && status !== 'IN_PROGRESS' && status !== 'COMPLETED')) {
      return res.status(403).json({
        success: false,
        error: 'TOPIC_LOCKED',
        message: 'This topic is locked. Complete prerequisite lessons and quizzes first.',
      });
    }

    // Generate single-use ticket
    const nonce = crypto.randomUUID();
    const expiresAt = Date.now() + 60000; // 60-second validity
    const payload = `${userId}:${topicId}:${nonce}:${expiresAt}`;
    const signature = crypto.createHmac('sha256', TICKET_SECRET).update(payload).digest('hex');
    const ticket = `${payload}.${signature}`;

    // Store nonce in Redis with 60s TTL
    const redis = getRedis();
    await redis.set(`ticket:${nonce}`, topicId, 'EX', 60);

    return res.json({
      success: true,
      topicId,
      ticket,
      streamUrl: `/api/v1/lessons/${topicId}?ticket=${encodeURIComponent(ticket)}`,
    });
  } catch (err) {
    console.error('[TICKET ERROR]', err);
    return res.status(500).json({ success: false, error: err.message });
  }
});

// GET /api/v1/lessons/:topicId?ticket=<ticket>
// Content Proxy & HTML Streamer
router.get('/lessons/:topicId', async (req, res) => {
  try {
    const topicId = req.params.topicId.toUpperCase();
    const ticket = req.query.ticket;

    if (!ticket) {
      return res.status(401).send('<h3>401 Unauthorized: Ephemeral ticket missing</h3>');
    }

    const dotIndex = ticket.lastIndexOf('.');
    if (dotIndex === -1) {
      return res.status(401).send('<h3>401 Unauthorized: Malformed ticket</h3>');
    }

    const payload = ticket.slice(0, dotIndex);
    const signature = ticket.slice(dotIndex + 1);

    // Validate signature
    const expectedSig = crypto.createHmac('sha256', TICKET_SECRET).update(payload).digest('hex');
    if (signature !== expectedSig) {
      return res.status(403).send('<h3>403 Forbidden: Invalid ticket signature</h3>');
    }

    const [userId, ticketTopicId, nonce, expiresAtStr] = payload.split(':');
    if (ticketTopicId !== topicId) {
      return res.status(403).send('<h3>403 Forbidden: Ticket topic mismatch</h3>');
    }

    if (Date.now() > parseInt(expiresAtStr, 10)) {
      return res.status(403).send('<h3>403 Forbidden: Ephemeral ticket expired</h3>');
    }

    // Verify and delete nonce from Redis (Single-use guarantee!)
    const redis = getRedis();
    const storedNonceTopic = await redis.get(`ticket:${nonce}`);
    if (!storedNonceTopic) {
      return res.status(403).send('<h3>403 Forbidden: Ticket already consumed or expired</h3>');
    }
    await redis.del(`ticket:${nonce}`);

    // Fetch raw lesson HTML from private storage
    const rawHtml = await getLessonHtml(topicId);
    if (!rawHtml) {
      return res.status(404).send(`<h3>404 Not Found: Lesson ${topicId}</h3>`);
    }

    // Inject anti-tampering security scripts into HTML
    const securityScript = generateAntiTamperScript({ userId, topicId, nonce });
    let transformedHtml = rawHtml;

    if (transformedHtml.includes('<head>')) {
      transformedHtml = transformedHtml.replace('<head>', `<head>${securityScript}`);
    } else {
      transformedHtml = `${securityScript}${transformedHtml}`;
    }

    // Rewrite relative asset URLs to authenticated proxy paths
    transformedHtml = transformedHtml.replace(/src="\.?\/?assets\/2_5d\/([^"]+)"/g, 'src="/api/v1/assets/2_5d/$1"');

    // Security Response Headers
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.setHeader('X-Frame-Options', 'SAMEORIGIN');
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('Cache-Control', 'private, no-cache, no-store, must-revalidate');

    return res.send(transformedHtml);
  } catch (err) {
    console.error('[LESSON PROXY ERROR]', err);
    return res.status(500).send('<h3>500 Internal Server Error</h3>');
  }
});

// POST /api/v1/lessons/:topicId/complete
router.post('/lessons/:topicId/complete', requireAuth, requireActiveEnrollment, async (req, res) => {
  try {
    const userId = req.user.id;
    const topicId = req.params.topicId.toUpperCase();

    // Mark current topic as COMPLETED
    await db.query(
      `UPDATE topic_progress
       SET status = 'COMPLETED', completed_at = NOW(), updated_at = NOW()
       WHERE user_id = $1 AND topic_id = $2`,
      [userId, topicId]
    );

    // Check if this topic is the end of a module
    if (MODULE_END_TOPICS[topicId]) {
      const moduleId = MODULE_END_TOPICS[topicId];
      await db.query(
        `UPDATE module_progress
         SET status = 'QUIZ_PENDING', updated_at = NOW()
         WHERE user_id = $1 AND module_id = $2`,
        [userId, moduleId]
      );

      return res.json({
        success: true,
        completedTopicId: topicId,
        nextAction: 'REQUIRE_MODULE_QUIZ',
        moduleId,
        message: `Module ${moduleId} complete. You must pass the Module ${moduleId} Quiz before advancing.`,
      });
    }

    // Otherwise unlock next sequential topic
    const nextTopicId = getNextTopicId(topicId);
    if (nextTopicId) {
      const nextMod = parseInt(nextTopicId.slice(1, 3), 10);
      await db.query(
        `INSERT INTO topic_progress (user_id, topic_id, module_id, status, unlocked_at)
         VALUES ($1, $2, $3, 'UNLOCKED', NOW())
         ON CONFLICT (user_id, topic_id) DO UPDATE
         SET status = CASE WHEN topic_progress.status = 'COMPLETED' THEN 'COMPLETED' ELSE 'UNLOCKED' END,
             unlocked_at = COALESCE(topic_progress.unlocked_at, NOW())`,
        [userId, nextTopicId, nextMod]
      );
    }

    return res.json({
      success: true,
      completedTopicId: topicId,
      nextUnlockedTopicId: nextTopicId,
    });
  } catch (err) {
    console.error('[TOPIC COMPLETE ERROR]', err);
    return res.status(500).json({ success: false, error: err.message });
  }
});

// GET /api/v1/assets/2_5d/:fileName
// Protected Visual Diorama Delivery
router.get('/assets/2_5d/:fileName', async (req, res) => {
  try {
    const fileName = req.params.fileName;
    const asset = await getAsset(fileName);

    if (!asset) {
      return res.status(404).send('Asset not found');
    }

    const ext = fileName.split('.').pop().toLowerCase();
    const mimeTypes = {
      jpg: 'image/jpeg',
      jpeg: 'image/jpeg',
      png: 'image/png',
      webp: 'image/webp',
      svg: 'image/svg+xml',
    };

    res.setHeader('Content-Type', mimeTypes[ext] || 'application/octet-stream');
    res.setHeader('Cache-Control', 'private, max-age=86400');
    return res.send(asset);
  } catch (err) {
    return res.status(500).send('Error loading asset');
  }
});

module.exports = router;
