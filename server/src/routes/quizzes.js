const express = require('express');
const router = express.Router();
const fs = require('fs');
const path = require('path');
const db = require('../db');
const { requireAuth, requireActiveEnrollment } = require('../auth');

// Load master answer keys into server memory
let masterKeysCache = {};
const masterKeysPath = path.join(__dirname, '..', '..', 'course_shell', 'mcqs', 'master_answer_keys.json');
if (fs.existsSync(masterKeysPath)) {
  try {
    const raw = JSON.parse(fs.readFileSync(masterKeysPath, 'utf-8'));
    for (const t of raw) {
      masterKeysCache[t.topic_id.toUpperCase()] = t;
    }
    console.log(`[QUIZ] Loaded ${Object.keys(masterKeysCache).length} topic answer keys into server memory.`);
  } catch (err) {
    console.error('[QUIZ] Failed to load master answer keys:', err.message);
  }
}

// Load final exam bank into server memory
let finalExamBank = { bank_a_signs: [], bank_b_laws: [] };
const examBankPath = path.join(__dirname, '..', '..', 'course_shell', 'mcqs', 'final_exam_bank.json');
if (fs.existsSync(examBankPath)) {
  try {
    finalExamBank = JSON.parse(fs.readFileSync(examBankPath, 'utf-8'));
    console.log(`[QUIZ] Loaded final exam bank: ${finalExamBank.bank_a_signs?.length} signs, ${finalExamBank.bank_b_laws?.length} laws.`);
  } catch (err) {
    console.error('[QUIZ] Failed to load final exam bank:', err.message);
  }
}

// GET /api/v1/quizzes/:moduleId
// Fetch sanitized questions for a module
router.get('/quizzes/:moduleId', requireAuth, requireActiveEnrollment, async (req, res) => {
  try {
    const moduleId = parseInt(req.params.moduleId, 10);
    const modPrefix = `L${String(moduleId).padStart(2, '0')}-`;

    const topicKeys = Object.keys(masterKeysCache).filter((k) => k.startsWith(modPrefix));
    if (topicKeys.length === 0) {
      return res.status(404).json({ success: false, error: 'MODULE_NOT_FOUND' });
    }

    const sanitizedQuestions = [];
    for (const tk of topicKeys) {
      const topicData = masterKeysCache[tk];
      for (const q of topicData.questions || []) {
        sanitizedQuestions.push({
          id: `${tk}_Q${q.number}`,
          topicId: tk,
          number: q.number,
          prompt: q.prompt,
          options: q.options,
          category: q.category,
          svg_key: q.svg_key || null,
        });
      }
    }

    // Limit to 10-15 random questions for the module quiz
    const shuffled = sanitizedQuestions.sort(() => 0.5 - Math.random()).slice(0, 10);

    return res.json({
      success: true,
      moduleId,
      title: `Module ${moduleId} Mastery Assessment`,
      passThresholdPercent: 70.0,
      totalQuestions: shuffled.length,
      questions: shuffled,
    });
  } catch (err) {
    return res.status(500).json({ success: false, error: err.message });
  }
});

// POST /api/v1/quizzes/submit
// Grade module quiz on server
router.post('/quizzes/submit', requireAuth, requireActiveEnrollment, async (req, res) => {
  try {
    const userId = req.user.id;
    const { moduleId, answers = {} } = req.body;

    const modId = parseInt(moduleId, 10);
    let totalQuestions = 0;
    let correctCount = 0;

    for (const [qid, selectedOption] of Object.entries(answers)) {
      totalQuestions++;
      // Format: L01-T01_Q1
      const parts = qid.split('_Q');
      const topicId = parts[0];
      const qNum = parseInt(parts[1], 10);

      const topicData = masterKeysCache[topicId];
      if (topicData) {
        const question = topicData.questions.find((q) => q.number === qNum);
        if (question && question.correct_option === parseInt(selectedOption, 10)) {
          correctCount++;
        }
      }
    }

    const scorePercentage = totalQuestions > 0 ? (correctCount / totalQuestions) * 100 : 0;
    const passed = scorePercentage >= 70.0;

    // Record quiz attempt
    await db.query(
      `INSERT INTO quiz_attempts (user_id, assessment_type, module_id, total_questions, correct_count, score_percentage, passed, student_responses_json, submitted_at)
       VALUES ($1, 'MODULE_QUIZ', $2, $3, $4, $5, $6, $7, NOW())`,
      [userId, modId, totalQuestions, correctCount, scorePercentage, passed, JSON.stringify(answers)]
    );

    let nextUnlockedTopicId = null;

    if (passed) {
      // Update module progress
      await db.query(
        `UPDATE module_progress
         SET status = 'COMPLETED', quiz_passed = 1, best_quiz_score = GREATEST(best_quiz_score, $3), completed_at = NOW(), updated_at = NOW()
         WHERE user_id = $1 AND module_id = $2`,
        [userId, modId, scorePercentage]
      );

      // Unlock first topic of next module (if modId < 9)
      if (modId < 9) {
        const nextMod = modId + 1;
        nextUnlockedTopicId = `L${String(nextMod).padStart(2, '0')}-T01`;
        await db.query(
          `INSERT INTO topic_progress (user_id, topic_id, module_id, status, unlocked_at)
           VALUES ($1, $2, $3, 'UNLOCKED', NOW())
           ON CONFLICT (user_id, topic_id) DO UPDATE
           SET status = CASE WHEN topic_progress.status = 'COMPLETED' THEN 'COMPLETED' ELSE 'UNLOCKED' END`,
          [userId, nextUnlockedTopicId, nextMod]
        );
        await db.query(
          `INSERT INTO module_progress (user_id, module_id, status)
           VALUES ($1, $2, 'IN_PROGRESS')
           ON CONFLICT (user_id, module_id) DO NOTHING`,
          [userId, nextMod]
        );
      }
    }

    return res.json({
      success: true,
      moduleId: modId,
      scorePercentage: Math.round(scorePercentage * 10) / 10,
      correctCount,
      totalQuestions,
      passed,
      passThresholdPercent: 70.0,
      nextUnlockedTopicId,
      message: passed
        ? `Congratulations! You passed Module ${modId} with ${Math.round(scorePercentage)}%.`
        : `You scored ${Math.round(scorePercentage)}%. A score of 70% is required to pass. Please review and try again.`,
    });
  } catch (err) {
    console.error('[QUIZ SUBMIT ERROR]', err);
    return res.status(500).json({ success: false, error: err.message });
  }
});

// GET /api/v1/exam/generate
// TDLR 16 TAC §84.503 Final Exam Generator (30 questions: 15 signs + 15 laws)
router.get('/exam/generate', requireAuth, requireActiveEnrollment, async (req, res) => {
  try {
    const signsBank = finalExamBank.bank_a_signs || [];
    const lawsBank = finalExamBank.bank_b_laws || [];

    // Shuffle and pick 15 from each
    const selectedSigns = [...signsBank].sort(() => 0.5 - Math.random()).slice(0, 15);
    const selectedLaws = [...lawsBank].sort(() => 0.5 - Math.random()).slice(0, 15);

    const fullExam = [...selectedSigns, ...selectedLaws];

    // Sanitize questions (strip correct_option and rationale)
    const sanitized = fullExam.map((q, idx) => ({
      number: idx + 1,
      id: q.id,
      domain: q.domain,
      category: q.category,
      prompt: q.prompt,
      options: q.options,
      svg_key: q.svg_key || null,
    }));

    return res.json({
      success: true,
      totalQuestions: 30,
      passThresholdPercent: 70.0, // 21 out of 30 required
      questions: sanitized,
    });
  } catch (err) {
    return res.status(500).json({ success: false, error: err.message });
  }
});

// POST /api/v1/exam/submit
// Grade TDLR Final Examination
router.post('/exam/submit', requireAuth, requireActiveEnrollment, async (req, res) => {
  try {
    const userId = req.user.id;
    const { answers = {} } = req.body;

    const allBank = [...(finalExamBank.bank_a_signs || []), ...(finalExamBank.bank_b_laws || [])];
    const bankMap = new Map(allBank.map((q) => [q.id, q]));

    let correctCount = 0;
    let totalQuestions = 0;

    for (const [qid, selectedOption] of Object.entries(answers)) {
      totalQuestions++;
      const q = bankMap.get(qid);
      if (q && q.correct_option === parseInt(selectedOption, 10)) {
        correctCount++;
      }
    }

    const scorePercentage = totalQuestions > 0 ? (correctCount / totalQuestions) * 100 : 0;
    const passed = scorePercentage >= 70.0 && totalQuestions >= 25; // 70% threshold

    // Verify minimum 21,600 instructional seconds
    const timeRes = await db.query(
      `SELECT SUM(instructional_seconds) as total FROM topic_progress WHERE user_id = $1`,
      [userId]
    );
    const totalSeconds = parseInt(timeRes.rows[0].total || '0', 10);
    const hasRequiredTime = totalSeconds >= 21600;

    // Record attempt
    await db.query(
      `INSERT INTO quiz_attempts (user_id, assessment_type, module_id, total_questions, correct_count, score_percentage, passed, student_responses_json, submitted_at)
       VALUES ($1, 'FINAL_EXAM', 9, $2, $3, $4, $5, $6, NOW())`,
      [userId, totalQuestions, correctCount, scorePercentage, passed, JSON.stringify(answers)]
    );

    return res.json({
      success: true,
      passed,
      correctCount,
      totalQuestions,
      scorePercentage: Math.round(scorePercentage * 10) / 10,
      hasRequiredInstructionalTime: hasRequiredTime,
      totalInstructionalHours: Math.round((totalSeconds / 3600) * 100) / 100,
      eligibleForCertificate: passed && hasRequiredTime,
      message: passed
        ? hasRequiredTime
          ? 'Congratulations! You passed the Texas Adult Driver Education Exam and completed all required instructional hours.'
          : `Exam passed (${correctCount}/${totalQuestions}), but you still have remaining instructional time before certificate issuance.`
        : `You scored ${Math.round(scorePercentage)}%. A passing score of 70% (21/30) is required.`,
    });
  } catch (err) {
    console.error('[EXAM SUBMIT ERROR]', err);
    return res.status(500).json({ success: false, error: err.message });
  }
});

module.exports = router;
