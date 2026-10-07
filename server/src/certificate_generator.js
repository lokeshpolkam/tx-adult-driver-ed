const PDFDocument = require('pdfkit');
const QRCode = require('qrcode');
const crypto = require('crypto');

async function generateCertificatePdf(certData) {
  return new Promise(async (resolve, reject) => {
    try {
      const doc = new PDFDocument({
        size: 'LETTER',
        layout: 'landscape',
        margins: { top: 36, bottom: 36, left: 36, right: 36 },
      });

      const buffers = [];
      doc.on('data', (chunk) => buffers.push(chunk));
      doc.on('end', () => resolve(Buffer.concat(buffers)));

      // Generate QR Code image data
      const qrDataUrl = await QRCode.toDataURL(certData.verificationUrl, {
        errorCorrectionLevel: 'H',
        margin: 1,
        width: 120,
      });
      const qrImageBuffer = Buffer.from(qrDataUrl.split(',')[1], 'base64');

      // Outer Border
      doc.rect(20, 20, 752, 572).lineWidth(3).strokeColor('#1E3A8A').stroke();
      doc.rect(26, 26, 740, 560).lineWidth(1).strokeColor('#D97706').stroke();

      // Header Banner
      doc.fontSize(22).font('Helvetica-Bold').fillColor('#1E3A8A').text('STATE OF TEXAS', 0, 50, { align: 'center' });
      doc.fontSize(12).font('Helvetica').fillColor('#4B5563').text('TEXAS DEPARTMENT OF LICENSING AND REGULATION (TDLR)', 0, 78, { align: 'center' });
      doc.fontSize(10).font('Helvetica-Bold').fillColor('#D97706').text('OFFICIAL CERTIFICATE OF COMPLETION — FORM ADE-1317', 0, 95, { align: 'center' });

      // Title
      doc.moveDown(1.5);
      doc.fontSize(26).font('Helvetica-Bold').fillColor('#111827').text('ADULT DRIVER EDUCATION', { align: 'center' });
      doc.fontSize(12).font('Helvetica').fillColor('#6B7280').text('Six (6) Clock Hour Instructional Course | 16 TAC §84.500', { align: 'center' });

      // Certify line
      doc.moveDown(1.2);
      doc.fontSize(12).font('Helvetica').fillColor('#374151').text('This certifies that the student named below has successfully completed the mandated course of instruction:', { align: 'center' });

      // Student Name
      doc.moveDown(0.8);
      doc.fontSize(24).font('Helvetica-Bold').fillColor('#1E3A8A').text(certData.studentLegalName.toUpperCase(), { align: 'center' });

      // Horizontal separator
      const yLine = doc.y + 10;
      doc.moveTo(150, yLine).lineTo(642, yLine).lineWidth(1).strokeColor('#CBD5E1').stroke();

      // Student & Completion Details Grid
      const col1X = 70;
      const col2X = 300;
      const col3X = 520;
      const startDetailsY = yLine + 20;

      doc.fontSize(10).font('Helvetica-Bold').fillColor('#4B5563');
      doc.text('Date of Birth:', col1X, startDetailsY);
      doc.font('Helvetica').fillColor('#111827').text(certData.studentDob || 'N/A', col1X + 80, startDetailsY);

      doc.font('Helvetica-Bold').fillColor('#4B5563').text('DL / SSN (Last 4):', col1X, startDetailsY + 20);
      doc.font('Helvetica').fillColor('#111827').text(`***-**-${certData.dlOrSsnLast4 || 'XXXX'}`, col1X + 100, startDetailsY + 20);

      doc.font('Helvetica-Bold').fillColor('#4B5563').text('Completion Date:', col2X, startDetailsY);
      doc.font('Helvetica').fillColor('#111827').text(certData.completionDate, col2X + 100, startDetailsY);

      doc.font('Helvetica-Bold').fillColor('#4B5563').text('Instructional Time:', col2X, startDetailsY + 20);
      doc.font('Helvetica').fillColor('#111827').text(`${certData.totalClockHours.toFixed(2)} Clock Hours`, col2X + 105, startDetailsY + 20);

      doc.font('Helvetica-Bold').fillColor('#4B5563').text('Final Exam Score:', col2X, startDetailsY + 40);
      doc.font('Helvetica').fillColor('#111827').text(`${certData.finalExamScore.toFixed(1)}% (Passed)`, col2X + 105, startDetailsY + 40);

      // School & Serial Information
      doc.font('Helvetica-Bold').fillColor('#4B5563').text('Certificate Serial #:', col3X, startDetailsY);
      doc.font('Helvetica-Bold').fillColor('#DC2626').text(certData.serialNumber, col3X, startDetailsY + 15);

      doc.font('Helvetica-Bold').fillColor('#4B5563').text('School License:', col3X, startDetailsY + 35);
      doc.font('Helvetica').fillColor('#111827').text(certData.tdlrSchoolCode || 'C3284', col3X, startDetailsY + 50);

      // Embed QR code for instant law enforcement verification
      doc.image(qrImageBuffer, 650, 430, { width: 90, height: 90 });
      doc.fontSize(7).font('Helvetica').fillColor('#6B7280').text('Scan to Verify with DPS', 645, 525, { width: 100, align: 'center' });

      // Verification Hash & Legal Footer
      const footerY = 510;
      doc.fontSize(8).font('Courier').fillColor('#6B7280').text(`Digital Verification Hash: ${certData.sha256Hash}`, 60, footerY);
      doc.fontSize(8).font('Helvetica').fillColor('#9CA3AF').text(
        'This certificate is an official legal record recognized by Texas DPS under 16 TAC §84.500 and TTC §521.1601. Any alteration constitutes a felony offense.',
        60,
        footerY + 15,
        { width: 570 }
      );

      doc.end();
    } catch (err) {
      reject(err);
    }
  });
}

function calculateCertHash(serialNumber, studentName, completionDate) {
  const content = `${serialNumber}:${studentName}:${completionDate}:TDLR-ADE-1317:C3284`;
  return crypto.createHash('sha256').update(content).digest('hex');
}

module.exports = {
  generateCertificatePdf,
  calculateCertHash,
};
