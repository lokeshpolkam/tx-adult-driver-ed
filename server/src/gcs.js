const { Storage } = require('@google-cloud/storage');
const fs = require('fs');
const path = require('path');

const storage = new Storage();
const CURRICULUM_BUCKET = process.env.CURRICULUM_BUCKET || 'tx-dmv-private-curriculum';
const CERTIFICATES_BUCKET = process.env.CERTIFICATES_BUCKET || 'tx-dmv-certificates';

async function getLessonHtml(topicId) {
  try {
    const bucket = storage.bucket(CURRICULUM_BUCKET);
    const file = bucket.file(`topics/${topicId}.html`);
    const [exists] = await file.exists();
    if (exists) {
      const [contents] = await file.download();
      return contents.toString('utf-8');
    }
  } catch (err) {
    console.warn(`[GCS] Error reading gs://${CURRICULUM_BUCKET}/topics/${topicId}.html:`, err.message);
  }

  // Local fallback
  const localPath = path.join(__dirname, '..', '..', 'course_shell', 'final_course_export', `${topicId}.html`);
  if (fs.existsSync(localPath)) {
    return fs.readFileSync(localPath, 'utf-8');
  }

  return null;
}

async function getAsset(fileName) {
  try {
    const bucket = storage.bucket(CURRICULUM_BUCKET);
    const file = bucket.file(`assets/2_5d/${fileName}`);
    const [exists] = await file.exists();
    if (exists) {
      const [contents] = await file.download();
      return contents;
    }
  } catch (err) {
    console.warn(`[GCS] Error reading asset gs://${CURRICULUM_BUCKET}/assets/2_5d/${fileName}:`, err.message);
  }

  // Local fallback
  const localPath = path.join(__dirname, '..', '..', 'course_shell', 'final_course_export', 'assets', '2_5d', fileName);
  if (fs.existsSync(localPath)) {
    return fs.readFileSync(localPath);
  }

  return null;
}

async function uploadCertificatePdf(serialNumber, buffer) {
  const bucket = storage.bucket(CERTIFICATES_BUCKET);
  const file = bucket.file(`certificates/${serialNumber}.pdf`);
  await file.save(buffer, {
    contentType: 'application/pdf',
    metadata: {
      cacheControl: 'private, max-age=86400',
    },
  });
  return `gs://${CERTIFICATES_BUCKET}/certificates/${serialNumber}.pdf`;
}

module.exports = {
  getLessonHtml,
  getAsset,
  uploadCertificatePdf,
  CURRICULUM_BUCKET,
  CERTIFICATES_BUCKET,
};
