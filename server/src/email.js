/**
 * TX-ADE Production Email Dispatcher
 * Manages transactional notifications:
 * 1. Clean Onboarding / Sign-up Welcome Email
 * 2. Payment Success & Enrollment Confirmation Receipt
 * 3. Payment Failed / Action Required Alert
 * 
 * Powered by Resend (official API) with fallback to SMTP / structured audit logger.
 */

const nodemailer = require('nodemailer');
const { Resend } = require('resend');

const resendApiKey = (process.env.RESEND_API_KEY || '').trim();
const resend = resendApiKey ? new Resend(resendApiKey) : null;

const EMAIL_FROM = process.env.EMAIL_FROM || 'Texas Adult Driver Education <onboarding@resend.dev>';
const CLIENT_URL = process.env.CLIENT_URL || 'https://tx-drive.vercel.app';

let transporter = null;

function getTransporter() {
  if (transporter) return transporter;

  const host = process.env.SMTP_HOST;
  const user = process.env.SMTP_USER;
  const pass = process.env.SMTP_PASS;
  const port = parseInt(process.env.SMTP_PORT || '587', 10);

  if (host && user && pass) {
    transporter = nodemailer.createTransport({
      host,
      port,
      secure: port === 465,
      auth: { user, pass },
    });
    console.log(`[EMAIL] SMTP Transporter connected to: ${host}:${port}`);
  } else {
    // Development / Fallback Mock Transporter that logs cleanly without failing
    transporter = {
      sendMail: async (mailOptions) => {
        console.log(`[EMAIL DISPATCHED] (Mock / Local Logger)`);
        console.log(`  To:      ${mailOptions.to}`);
        console.log(`  From:    ${mailOptions.from}`);
        console.log(`  Subject: ${mailOptions.subject}`);
        return { messageId: `mock_${Date.now()}` };
      },
    };
    console.log('[EMAIL] Using structured audit logger fallback.');
  }

  return transporter;
}

/**
 * Universal Email Dispatcher: Resend first, SMTP/Mock fallback
 */
async function dispatchEmail({ to, subject, html }) {
  if (resend) {
    try {
      const response = await resend.emails.send({
        from: EMAIL_FROM,
        to,
        subject,
        html,
      });

      if (response.error) {
        console.error(`[RESEND API ERROR] Failed to send to ${to}:`, response.error.message || response.error);
        throw new Error(response.error.message || 'Resend API returned an error');
      }

      console.log(`[EMAIL DISPATCHED via RESEND] To: ${to} | ID: ${response.data?.id}`);
      return { success: true, messageId: response.data?.id, provider: 'resend' };
    } catch (err) {
      console.warn(`[RESEND FAILED] Falling back to SMTP/Mock:`, err.message);
    }
  }

  const mailer = getTransporter();
  try {
    const info = await mailer.sendMail({
      from: EMAIL_FROM,
      to,
      subject,
      html,
    });
    console.log(`[EMAIL DISPATCHED via SMTP/MOCK] To: ${to} | ID: ${info.messageId}`);
    return { success: true, messageId: info.messageId, provider: 'smtp' };
  } catch (err) {
    console.error(`[EMAIL ERROR] Failed to send email to ${to}:`, err.message);
    return { success: false, error: err.message };
  }
}

/**
 * Standard Email Wrapper Template with Texas State Driver Ed styling
 */
function wrapTemplate({ title, preheader, bodyContent }) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title}</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #070a10; margin: 0; padding: 24px; color: #1f2937; }
    .container { max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.15); }
    .header { background: linear-gradient(135deg, #070a10 0%, #111726 100%); padding: 32px 36px; text-align: left; border-bottom: 3px solid #e87522; }
    .badge { display: inline-block; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: #10b981; background: rgba(16, 185, 129, 0.15); padding: 4px 8px; border-radius: 4px; margin-bottom: 8px; }
    .brand-title { color: #ffffff; font-size: 20px; font-weight: 900; margin: 0; text-transform: uppercase; letter-spacing: -0.5px; }
    .brand-sub { color: #9ca3af; font-size: 11px; margin-top: 4px; font-family: monospace; }
    .content { padding: 36px; line-height: 1.6; font-size: 15px; color: #374151; }
    .btn { display: inline-block; background: #e87522; color: #ffffff !important; text-decoration: none; padding: 14px 28px; border-radius: 8px; font-weight: 700; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px; margin: 20px 0; }
    .receipt-box { background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 12px; padding: 20px; margin: 20px 0; }
    .receipt-row { display: flex; justify-content: space-between; padding: 6px 0; font-size: 13px; font-family: monospace; }
    .footer { background: #f3f4f6; padding: 24px 36px; text-align: center; font-size: 12px; color: #6b7280; font-family: monospace; border-top: 1px solid #e5e7eb; }
  </style>
</head>
<body>
  <div style="display:none;font-size:1px;color:#333;line-height:1px;max-height:0px;max-width:0px;opacity:0;overflow:hidden;">
    ${preheader}
  </div>
  <div class="container">
    <div class="header">
      <div class="badge">TDLR Approved · State of Texas</div>
      <div class="brand-title">Texas Adult Driver Education</div>
      <div class="brand-sub">Course ADE-1317 · School License #C3284</div>
    </div>
    <div class="content">
      ${bodyContent}
    </div>
    <div class="footer">
      <p style="margin: 0 0 8px 0; font-weight: bold; color: #111827;">Texas Department of Licensing and Regulation (TDLR) Licensed School #C3284</p>
      <p style="margin: 0 0 8px 0;">Approved under 16 TAC § 84.500 & Texas Transportation Code § 521.1601</p>
      <p style="margin: 0;">Support: <a href="mailto:support@texasade.org" style="color: #e87522;">support@texasade.org</a> · Austin, Texas</p>
    </div>
  </div>
</body>
</html>`;
}

/**
 * 1. Clean Onboarding / Sign-up Welcome Email
 */
async function sendWelcomeEmail({ email, fullName }) {
  const name = fullName || 'Student';

  const bodyContent = `
    <h2 style="color: #111827; margin-top: 0; font-size: 22px;">Welcome to Texas Adult Driver Ed, ${name}!</h2>
    <p>Your student profile has been created successfully. You are now registered to complete your mandatory 6-hour Texas Adult Driver Education course (ADE-1317).</p>
    
    <div style="background: #eff6ff; border-left: 4px solid #3b82f6; padding: 14px 18px; margin: 20px 0; border-radius: 0 8px 8px 0;">
      <p style="margin: 0; font-size: 13px; color: #1e40af; font-weight: 600;">FREE PREVIEW UNLOCKED:</p>
      <p style="margin: 4px 0 0 0; font-size: 13px; color: #1e3a8a;">Module 1 is 100% unlocked for your free preview right now. Complete topic 1 to begin accumulating your verified clock hours.</p>
    </div>

    <h3 style="color: #111827; font-size: 16px; margin: 24px 0 12px 0;">What to expect:</h3>
    <ul style="padding-left: 20px; margin: 0; color: #4b5563;">
      <li style="margin-bottom: 8px;"><strong>100% Online & Self-Paced:</strong> Complete your 6 clock hours on your phone, tablet, or laptop. Your progress saves automatically.</li>
      <li style="margin-bottom: 8px;"><strong>Skip the DPS Written Test:</strong> The official written knowledge test is included in Module 9. Score 70%+ to waive the test at DPS.</li>
      <li style="margin-bottom: 8px;"><strong>Official Form ADE-1317:</strong> Download your official state certificate immediately upon exam completion.</li>
    </ul>

    <div style="text-align: center; margin: 32px 0;">
      <a href="${CLIENT_URL}/player.html" class="btn">Enter Virtual Classroom</a>
    </div>

    <p style="font-size: 13px; color: #6b7280; margin-top: 24px;">
      If you did not create this account, please disregard this email or contact us at <a href="mailto:support@texasade.org" style="color: #e87522;">support@texasade.org</a>.
    </p>
  `;

  const html = wrapTemplate({
    title: 'Welcome to Texas Adult Driver Education',
    preheader: 'Your student account is active. Enter the virtual classroom to begin Module 1.',
    bodyContent,
  });

  return await dispatchEmail({
    to: email,
    subject: 'Welcome to Texas Adult Driver Education (TDLR ADE-1317)',
    html,
  });
}

/**
 * 2. Payment Success Receipt & Enrollment Confirmation Email
 */
async function sendPaymentSuccessEmail({ email, fullName, amountCents = 0, sessionId, tier = 'STANDARD', couponCode = null, rushPriceCents = 0 }) {
  const name = fullName || 'Student';
  const isFree = amountCents === 0;
  const formattedAmount = `$${(amountCents / 100).toFixed(2)}`;
  const orderRef = sessionId ? sessionId.slice(-12).toUpperCase() : `TX-${Date.now().toString().slice(-8)}`;

  const badgeHtml = isFree
    ? `<span style="display: inline-block; background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: bold; font-family: monospace;">
        ✓ 100% TUITION WAIVER APPLIED & ENROLLMENT ACTIVE
       </span>`
    : `<span style="display: inline-block; background: #ecfdf5; color: #059669; border: 1px solid #a7f3d0; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: bold; font-family: monospace;">
        ✓ PAYMENT RECEIVED & ENROLLMENT ACTIVE
       </span>`;

  const headerTitle = isFree ? 'Enrollment Confirmation & Tuition Waiver Receipt' : 'Enrollment Confirmation & Receipt';
  const introText = isFree
    ? `Your 100% tuition waiver${couponCode ? ` (Code: ${couponCode})` : ''} has been activated successfully. Your student profile has been granted <strong>Full Active Access</strong> to all 9 modules, state quizzes, and the official final DPS exam.`
    : `Your payment was completed successfully via Stripe. Your student profile has been granted <strong>Full Active Access</strong> to all 9 modules, state quizzes, and the official final DPS exam.`;

  const promoRow = couponCode
    ? `<tr>
        <td style="padding: 6px 0; color: #6b7280;">Promo / Waiver Code:</td>
        <td style="padding: 6px 0; text-align: right; font-family: monospace; font-weight: bold; color: #059669;">${couponCode}</td>
       </tr>`
    : '';

  const bodyContent = `
    <div style="text-align: center; margin-bottom: 24px;">
      ${badgeHtml}
      <h2 style="color: #111827; margin: 16px 0 4px 0; font-size: 24px;">${headerTitle}</h2>
      <p style="color: #6b7280; font-size: 14px; margin: 0;">Thank you for your enrollment, ${name}!</p>
    </div>

    <p>${introText}</p>

    <!-- Receipt Details -->
    <div class="receipt-box">
      <div style="font-weight: bold; font-size: 12px; color: #4b5563; text-transform: uppercase; margin-bottom: 12px; border-bottom: 1px solid #e5e7eb; padding-bottom: 6px;">
        Order Details
      </div>
      <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
        <tr>
          <td style="padding: 6px 0; color: #6b7280;">Order Reference:</td>
          <td style="padding: 6px 0; text-align: right; font-family: monospace; font-weight: bold; color: #111827;">${orderRef}</td>
        </tr>
        <tr>
          <td style="padding: 6px 0; color: #6b7280;">Course:</td>
          <td style="padding: 6px 0; text-align: right; font-weight: bold; color: #111827;">Texas Adult Driver Ed (ADE-1317)</td>
        </tr>
        <tr>
          <td style="padding: 6px 0; color: #6b7280;">Delivery Tier:</td>
          <td style="padding: 6px 0; text-align: right; font-weight: bold; color: #111827;">${tier === 'EXPRESS' ? 'Same-Day Priority Express' : 'Standard Delivery'}</td>
        </tr>
        ${promoRow}
        <tr>
          <td style="padding: 6px 0; color: #6b7280;">DPS Written Test Waiver:</td>
          <td style="padding: 6px 0; text-align: right; font-weight: bold; color: #059669;">Included ($0.00)</td>
        </tr>
        <tr style="border-top: 1px solid #e5e7eb;">
          <td style="padding: 10px 0 0 0; font-weight: bold; font-size: 15px; color: #111827;">Total Paid:</td>
          <td style="padding: 10px 0 0 0; text-align: right; font-weight: 900; font-size: 18px; color: #e87522;">${isFree ? '$0.00 (Tuition Waiver)' : formattedAmount}</td>
        </tr>
      </table>
    </div>

    <h3 style="color: #111827; font-size: 15px; margin: 24px 0 8px 0;">Next Steps to Claim Your Texas Driver License:</h3>
    <ol style="padding-left: 20px; margin: 0; color: #4b5563; font-size: 14px; line-height: 1.8;">
      <li>Log into your classroom and complete the 6 instructional clock hours.</li>
      <li>In Module 9, Topic 1, verify your identity via the Personal Verification Questions (PVQ).</li>
      <li>Pass the 30-question final exam in Module 9, Topic 2 (70% or higher).</li>
      <li>Instantly download your official <strong>Form ADE-1317 Certificate</strong> to present at your DPS appointment!</li>
    </ol>

    <div style="text-align: center; margin: 32px 0;">
      <a href="${CLIENT_URL}/player.html" class="btn">Resume Course in Classroom</a>
    </div>

    <p style="font-size: 12px; color: #9ca3af; text-align: center;">Keep this receipt for your personal tax or educational records.</p>
  `;

  const html = wrapTemplate({
    title: isFree
      ? 'Enrollment Confirmation: Texas Adult Driver Education (ADE-1317)'
      : 'Payment Confirmation: Texas Adult Driver Education (ADE-1317)',
    preheader: isFree
      ? `Enrollment confirmed with 100% Tuition Waiver. All 9 modules are unlocked.`
      : `Payment confirmed for ${formattedAmount}. All 9 modules are unlocked.`,
    bodyContent,
  });

  return await dispatchEmail({
    to: email,
    subject: isFree
      ? `Enrollment Confirmed: Texas Adult Driver Ed (ADE-1317) [${orderRef}]`
      : `Receipt & Enrollment Confirmed: Texas Adult Driver Ed (ADE-1317) [${orderRef}]`,
    html,
  });
}

/**
 * 3. Payment Failed / Action Required Notification Email
 */
async function sendPaymentFailedEmail({ email, fullName, reason = 'Card was declined', checkoutUrl }) {
  const name = fullName || 'Student';
  const retryUrl = checkoutUrl || `${CLIENT_URL}/checkout.html`;

  const bodyContent = `
    <div style="text-align: center; margin-bottom: 24px;">
      <span style="display: inline-block; background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: bold; font-family: monospace;">
        ⚠️ PAYMENT UNSUCCESSFUL
      </span>
      <h2 style="color: #111827; margin: 16px 0 4px 0; font-size: 24px;">Action Required: Course Enrollment</h2>
      <p style="color: #6b7280; font-size: 14px; margin: 0;">Hello ${name}, we encountered an issue processing your payment.</p>
    </div>

    <p>We attempted to process your enrollment for the Texas Adult Driver Education course (ADE-1317), but the transaction could not be completed.</p>

    <div style="background: #fff1f2; border-left: 4px solid #e11d48; padding: 14px 18px; margin: 20px 0; border-radius: 0 8px 8px 0;">
      <p style="margin: 0; font-size: 13px; color: #9f1239; font-weight: bold;">DECLINE REASON:</p>
      <p style="margin: 4px 0 0 0; font-size: 13px; color: #881337;">${reason}. Your card has not been billed.</p>
    </div>

    <p>Don't worry—your progress and account details have been securely saved. You can complete your enrollment anytime using a different debit card, credit card, Apple Pay, or Google Pay.</p>

    <div style="text-align: center; margin: 32px 0;">
      <a href="${retryUrl}" class="btn" style="background: #dc2626;">Retry Payment Securely</a>
    </div>

    <p style="font-size: 13px; color: #6b7280;">
      Need assistance? Reply directly to this email or contact our Austin support team at <a href="mailto:support@texasade.org" style="color: #e87522;">support@texasade.org</a>.
    </p>
  `;

  const html = wrapTemplate({
    title: 'Payment Issue: Texas Adult Driver Education',
    preheader: 'Your payment could not be processed. Click here to review your enrollment.',
    bodyContent,
  });

  return await dispatchEmail({
    to: email,
    subject: 'Action Required: Your Texas Adult Driver Ed Payment Could Not Be Processed',
    html,
  });
}

/**
 * 4. Admin Access Email Invitation
 */
async function sendAdminInvitationEmail({ email, inviteUrl }) {
  const bodyContent = `
    <p style="font-size: 15px; color: #1E293B; line-height: 1.6; margin-top: 0;">Hi,</p>
    <p style="font-size: 15px; color: #1E293B; line-height: 1.6;">
      You’ve been invited to access the admin area. Click below to sign up with Google using <strong>${email}</strong>.
    </p>

    <div style="text-align: center; margin: 32px 0;">
      <a href="${inviteUrl}" class="btn" style="background: #E87522; color: #FFFFFF; font-weight: 700; text-decoration: none; padding: 14px 28px; border-radius: 8px; display: inline-block;">Accept invitation</a>
    </div>

    <p style="font-size: 13px; color: #64748B; line-height: 1.5;">
      This link expires in 24 hours and can only be used once. If you weren’t expecting this invitation, you can ignore this email.
    </p>
  `;

  const html = wrapTemplate({
    title: 'Admin Invitation: Texas Adult Driver Education',
    preheader: 'You have been invited to become an administrator.',
    bodyContent,
  });

  return await dispatchEmail({
    to: email,
    subject: 'You’ve been invited to become an admin',
    html,
  });
}

module.exports = {
  sendWelcomeEmail,
  sendPaymentSuccessEmail,
  sendPaymentFailedEmail,
  sendAdminInvitationEmail,
};
