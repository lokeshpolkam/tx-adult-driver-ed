const express = require('express');
const router = express.Router();
const db = require('../db');
const { requireAuth, requireActiveEnrollment } = require('../auth');
const { generateCertificatePdf, calculateCertHash } = require('../certificate_generator');
const { uploadCertificatePdf, CERTIFICATES_BUCKET } = require('../gcs');
const { Storage } = require('@google-cloud/storage');

const storage = new Storage();

// GET /api/v1/certificates/me
// Retrieve or generate official TDLR certificate
router.get('/me', requireAuth, requireActiveEnrollment, async (req, res) => {
  try {
    const userId = req.user.id;

    // 1. Check if user already has an issued certificate
    const existingCert = await db.query(
      `SELECT * FROM certificates WHERE user_id = $1`,
      [userId]
    );

    if (existingCert.rows.length > 0) {
      const c = existingCert.rows[0];
      return res.json({
        success: true,
        certificate: {
          serialNumber: c.serial_number,
          studentLegalName: c.student_legal_name,
          completionDate: c.completion_date,
          totalClockHours: c.total_instructional_hours,
          finalExamScore: c.final_exam_score,
          sha256Hash: c.sha256_hash,
          verificationUrl: c.verification_url,
          downloadUrl: `/api/v1/certificates/download/${c.serial_number}`,
        },
      });
    }

    // 2. Validate completion eligibility
    // A. 75 topics completed
    const topicsRes = await db.query(
      `SELECT COUNT(*) as count FROM topic_progress WHERE user_id = $1 AND status = 'COMPLETED'`,
      [userId]
    );
    const completedTopics = parseInt(topicsRes.rows[0].count, 10);
    if (completedTopics < 75) {
      return res.status(403).json({
        success: false,
        error: 'CURRICULUM_INCOMPLETE',
        message: `You have completed ${completedTopics} of 75 required topics.`,
      });
    }

    // B. Minimum 6 hours (21,600s) instructional time
    const timeRes = await db.query(
      `SELECT SUM(instructional_seconds) as total FROM topic_progress WHERE user_id = $1`,
      [userId]
    );
    const totalSeconds = parseInt(timeRes.rows[0].total || '0', 10);
    if (totalSeconds < 21600) {
      return res.status(403).json({
        success: false,
        error: 'INSTRUCTIONAL_TIME_INSUFFICIENT',
        message: `Mandatory 6 clock hours required. Current verified time: ${(totalSeconds / 3600).toFixed(2)} hours.`,
      });
    }

    // C. Final Exam passed
    const examRes = await db.query(
      `SELECT score_percentage, passed FROM quiz_attempts
       WHERE user_id = $1 AND assessment_type = 'FINAL_EXAM' AND passed = TRUE
       ORDER BY submitted_at DESC LIMIT 1`,
      [userId]
    );
    if (examRes.rows.length === 0) {
      return res.status(403).json({
        success: false,
        error: 'FINAL_EXAM_NOT_PASSED',
        message: 'Passing the 30-question final examination (>= 70%) is required before certificate generation.',
      });
    }

    // 3. Generate sequential certificate serial number
    const countRes = await db.query(`SELECT COUNT(*) as count FROM certificates`);
    const nextSeq = String(parseInt(countRes.rows[0].count, 10) + 1).padStart(5, '0');
    const serialNumber = `ADE1317-2026-${nextSeq}`;

    // 4. Fetch user details
    const userRes = await db.query(`SELECT * FROM users WHERE id = $1`, [userId]);
    const user = userRes.rows[0];

    // Fetch active enrollment
    const enrollRes = await db.query(`SELECT id, tier FROM enrollments WHERE user_id = $1 AND status = 'ACTIVE' LIMIT 1`, [userId]);
    const enrollment = enrollRes.rows[0];

    const studentLegalName = user.legal_first_name && user.legal_last_name
      ? `${user.legal_first_name} ${user.legal_last_name}`
      : user.full_name;

    const completionDate = new Date().toISOString().split('T')[0];
    const totalClockHours = Math.max(totalSeconds / 3600, 6.0);
    const finalExamScore = examRes.rows[0].score_percentage;
    const sha256Hash = calculateCertHash(serialNumber, studentLegalName, completionDate);
    const verificationUrl = `https://api.texasade.org/api/v1/public/verify/${serialNumber}`;

    // 5. Generate PDF
    const pdfBuffer = await generateCertificatePdf({
      serialNumber,
      tdlrSchoolCode: 'C3284',
      studentLegalName,
      studentDob: user.date_of_birth ? String(user.date_of_birth) : 'On File',
      dlOrSsnLast4: user.dl_or_ssn_last4 || 'On File',
      completionDate,
      totalClockHours,
      finalExamScore,
      sha256Hash,
      verificationUrl,
    });

    // 6. Upload PDF to GCS
    let gcsKey = `certificates/${serialNumber}.pdf`;
    try {
      gcsKey = await uploadCertificatePdf(serialNumber, pdfBuffer);
    } catch (gcsErr) {
      console.warn('[CERT] Could not upload to GCS, saving locally or continuing:', gcsErr.message);
    }

    // 7. Insert certificate record
    await db.query(
      `INSERT INTO certificates (
        user_id, enrollment_id, serial_number, tdlr_school_code,
        student_legal_name, student_dob, dl_or_ssn_last4, completion_date,
        total_instructional_hours, final_exam_score, pdf_gcs_key, sha256_hash,
        verification_url, delivery_tier
      ) VALUES ($1, $2, $3, 'C3284', $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)`,
      [
        userId,
        enrollment?.id,
        serialNumber,
        studentLegalName,
        user.date_of_birth || '2000-01-01',
        user.dl_or_ssn_last4 || '0000',
        completionDate,
        totalClockHours,
        finalExamScore,
        gcsKey,
        sha256Hash,
        verificationUrl,
        enrollment?.tier || 'STANDARD',
      ]
    );

    return res.json({
      success: true,
      message: 'Certificate issued successfully!',
      certificate: {
        serialNumber,
        studentLegalName,
        completionDate,
        totalClockHours,
        finalExamScore,
        sha256Hash,
        verificationUrl,
        downloadUrl: `/api/v1/certificates/download/${serialNumber}`,
      },
    });
  } catch (err) {
    console.error('[CERT GENERATION ERROR]', err);
    return res.status(500).json({ success: false, error: err.message });
  }
});

// GET /api/v1/certificates/download/:serialNumber
router.get('/download/:serialNumber', requireAuth, async (req, res) => {
  try {
    const serial = req.params.serialNumber;
    const certRes = await db.query(`SELECT * FROM certificates WHERE serial_number = $1`, [serial]);

    if (certRes.rows.length === 0) {
      return res.status(404).send('Certificate not found');
    }

    const cert = certRes.rows[0];
    if (cert.user_id !== req.user.id && req.user.role !== 'ADMIN') {
      return res.status(403).send('Forbidden');
    }

    // Attempt download from GCS or regenerate on the fly
    try {
      const bucket = storage.bucket(CERTIFICATES_BUCKET);
      const file = bucket.file(`certificates/${serial}.pdf`);
      const [exists] = await file.exists();
      if (exists) {
        res.setHeader('Content-Type', 'application/pdf');
        res.setHeader('Content-Disposition', `attachment; filename="${serial}.pdf"`);
        return file.createReadStream().pipe(res);
      }
    } catch (gcsErr) {}

    // Fallback: regenerate on the fly
    const pdfBuffer = await generateCertificatePdf({
      serialNumber: cert.serial_number,
      tdlrSchoolCode: cert.tdlr_school_code,
      studentLegalName: cert.student_legal_name,
      studentDob: String(cert.student_dob),
      dlOrSsnLast4: cert.dl_or_ssn_last4,
      completionDate: String(cert.completion_date),
      totalClockHours: cert.total_instructional_hours,
      finalExamScore: cert.final_exam_score,
      sha256Hash: cert.sha256_hash,
      verificationUrl: cert.verification_url,
    });

    res.setHeader('Content-Type', 'application/pdf');
    res.setHeader('Content-Disposition', `attachment; filename="${serial}.pdf"`);
    return res.send(pdfBuffer);
  } catch (err) {
    return res.status(500).send('Download error');
  }
});

// GET /api/v1/public/verify/:serialNumber
// Public Law Enforcement & DPS Verification Endpoint
router.get('/verify/:serialNumber', async (req, res) => {
  try {
    const serial = req.params.serialNumber;
    const certRes = await db.query(
      `SELECT serial_number, student_legal_name, completion_date, tdlr_school_code, total_instructional_hours, sha256_hash
       FROM certificates WHERE serial_number = $1`,
      [serial]
    );

    if (certRes.rows.length === 0) {
      return res.status(404).json({
        valid: false,
        serialNumber: serial,
        message: 'No certificate found with this serial number. Record not recognized by Texas DPS.',
      });
    }

    const c = certRes.rows[0];
    return res.json({
      valid: true,
      serialNumber: c.serial_number,
      studentLegalName: c.student_legal_name,
      schoolLicense: `TDLR School #${c.tdlr_school_code}`,
      courseApproval: 'TDLR Course ADE-1317 (Texas Adult Driver Education)',
      completionDate: c.completion_date,
      totalInstructionalHours: `${c.total_instructional_hours} Hours`,
      status: 'OFFICIALLY_RECORDED_AND_VALID',
      sha256Hash: c.sha256_hash,
    });
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
});

module.exports = router;
