/**
 * TX-ADE Cloud Synchronization & TDLR Compliance Bridge
 * Connects the frontend to the Cloud Run API backend:
 * - Google Sign-In & Session Persistence
 * - Stripe Payment Checkout
 * - Server-Verified 30s Heartbeats & Idle Pausing
 * - PVQ 90-Second Identity Challenges
 * - Ephemeral Ticket Lesson Gating
 */

const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'https://tx-ade-api-1004296326114.us-central1.run.app'
  : 'https://tx-ade-api-1004296326114.us-central1.run.app';

let currentUser = null;
let currentProgress = null;
let heartbeatTimer = null;
let pvqCountdownInterval = null;

// Initialize Google Sign-In and check session on load
async function initCloudSync() {
  console.log('[CLOUD SYNC] Initializing connection to:', API_BASE_URL);
  
  // Check active session
  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/auth/me`, {
      credentials: 'include',
    });
    if (res.ok) {
      const data = await res.json();
      if (data.success && data.user) {
        onUserAuthenticated(data.user);
        return;
      }
    }
  } catch (err) {
    console.warn('[CLOUD SYNC] No existing session or offline:', err.message);
  }

  // Not signed in: trigger mandatory state sign-in modal
  if (typeof window.showMandatoryAuthModal === 'function') {
    window.showMandatoryAuthModal();
  }
  renderGoogleSignInButton();
}

// Render Google Identity Services button
function renderGoogleSignInButton() {
  const container = document.getElementById('google-signin-container');
  const mandatoryContainer = document.getElementById('mandatory-google-signin');

  if (window.google && window.google.accounts) {
    window.google.accounts.id.initialize({
      client_id: window.__GOOGLE_CLIENT_ID__ || '1004296326114-dq4t23m4evubp6jv6jovjd955ju808jc.apps.googleusercontent.com',
      callback: handleGoogleCredentialResponse,
      auto_select: false,
    });

    if (container) {
      window.google.accounts.id.renderButton(container, {
        theme: 'outline',
        size: 'medium',
        type: 'standard',
        shape: 'rectangular',
        text: 'signin_with',
        logo_alignment: 'left',
      });
    }

    if (mandatoryContainer) {
      window.google.accounts.id.renderButton(mandatoryContainer, {
        theme: 'filled_blue',
        size: 'large',
        type: 'standard',
        shape: 'pill',
        text: 'signin_with',
        logo_alignment: 'left',
        width: 280,
      });
    }
  }
}

// Callback when student selects Google Account
async function handleGoogleCredentialResponse(response) {
  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/auth/google`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ id_token: response.credential }),
    });

    const data = await res.json();
    if (data.success && data.user) {
      onUserAuthenticated(data.user);
    } else {
      alert('Sign in failed: ' + (data.message || 'Unknown error'));
    }
  } catch (err) {
    alert('Network error during Google Sign-In: ' + err.message);
  }
}

// Handle successful authentication
async function onUserAuthenticated(user) {
  currentUser = user;
  console.log('[CLOUD SYNC] Authenticated as:', user.email);

  // Update header UI
  const badgeEl = document.getElementById('user-profile-badge');
  const nameEl = document.getElementById('user-display-name');
  const avatarEl = document.getElementById('user-avatar');

  if (badgeEl) {
    badgeEl.classList.remove('hidden');
    badgeEl.classList.add('flex');
  }
  if (nameEl) {
    nameEl.textContent = user.fullName || user.email;
  }
  if (avatarEl) {
    if (user.profileImage) {
      avatarEl.innerHTML = `<img src="${user.profileImage}" alt="${user.fullName}" class="w-full h-full object-cover">`;
    } else {
      const initials = (user.fullName || user.email).slice(0, 2).toUpperCase();
      avatarEl.textContent = initials;
    }
    avatarEl.title = `${user.fullName} (${user.email})`;
  }

  // Hide login button and mandatory gate
  const signinContainer = document.getElementById('google-signin-container');
  if (signinContainer) signinContainer.style.display = 'none';

  if (typeof window.hideMandatoryAuthModal === 'function') {
    window.hideMandatoryAuthModal(user);
  }

  // Check enrollment
  if (user.enrollmentStatus !== 'ACTIVE') {
    showPaymentBanner();
    if (typeof window.setEnrollmentStatus === 'function') {
      window.setEnrollmentStatus(false);
    }
  } else {
    hidePaymentBanner();
    startHeartbeatService();
    if (typeof window.setEnrollmentStatus === 'function') {
      window.setEnrollmentStatus(true);
    }
  }

  // Sync progress
  await syncProgressFromCloud();
}

// Fetch student progress from Cloud SQL
async function syncProgressFromCloud() {
  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/student/progress`, {
      credentials: 'include',
    });
    if (res.ok) {
      const { data } = await res.json();
      currentProgress = data;

      if (data.enrollmentStatus === 'ACTIVE' && typeof window.setEnrollmentStatus === 'function') {
        window.setEnrollmentStatus(true);
      }

      // Update timer and progress bar
      if (typeof updateCourseMetrics === 'function') {
        updateCourseMetrics(data.completedTopicsCount, data.totalInstructionalSeconds);
      }

      console.log(`[CLOUD SYNC] Synced: ${data.completedTopicsCount}/75 topics, ${data.totalInstructionalSeconds}s`);
    }
  } catch (err) {
    console.warn('[CLOUD SYNC] Progress sync failed:', err.message);
  }
}

// 30-Second Heartbeat Engine
function startHeartbeatService() {
  if (heartbeatTimer) clearInterval(heartbeatTimer);

  heartbeatTimer = setInterval(async () => {
    // Only send heartbeat if window is focused and user is not idle
    if (document.hidden || window.__USER_IDLE__) return;

    const currentTopicId = window.__ACTIVE_TOPIC_ID__ || 'L01-T01';

    try {
      const res = await fetch(`${API_BASE_URL}/api/v1/student/heartbeat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ topicId: currentTopicId, deltaSeconds: 30 }),
      });

      if (res.ok) {
        const data = await res.json();
        if (data.pvqDue && data.pvqChallenge) {
          triggerPvqChallengeModal(data.pvqChallenge);
        }
      }
    } catch (err) {
      console.warn('[HEARTBEAT] Ping failed:', err.message);
    }
  }, 30000);
}

// Trigger PVQ Challenge Modal (Mandated 90s timeout)
function triggerPvqChallengeModal(challenge) {
  // Pause lesson iframe
  const frame = document.getElementById('content-frame');
  if (frame) frame.style.pointerEvents = 'none';

  let remainingSeconds = challenge.timeoutSeconds || 90;
  const modal = document.createElement('div');
  modal.id = 'pvq-challenge-modal';
  modal.className = 'fixed inset-0 bg-black/70 backdrop-blur-md z-50 flex items-center justify-center p-4';
  modal.innerHTML = `
    <div class="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl border-2 border-amber-500 font-sans">
      <div class="flex items-center justify-between pb-3 border-b">
        <span class="text-xs font-mono font-bold text-amber-700 bg-amber-100 px-2.5 py-1 rounded">TDLR IDENTITY VERIFICATION</span>
        <span id="pvq-timer" class="text-sm font-mono font-bold text-red-600">01:30</span>
      </div>
      <h3 class="text-base font-bold text-gray-900 mt-4">${challenge.questionPrompt}</h3>
      <p class="text-xs text-gray-500 mt-1">State law mandates verification within 90 seconds.</p>
      <input type="text" id="pvq-input" class="w-full mt-4 p-3 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-amber-500 outline-none" placeholder="Enter your response...">
      <div class="mt-4 flex gap-2">
        <button id="pvq-submit" class="flex-1 bg-amber-600 hover:bg-amber-700 text-white font-bold py-2.5 rounded-lg text-sm">SUBMIT</button>
      </div>
    </div>
  `;
  document.body.appendChild(modal);

  const timerEl = document.getElementById('pvq-timer');
  const inputEl = document.getElementById('pvq-input');
  inputEl.focus();

  pvqCountdownInterval = setInterval(() => {
    remainingSeconds--;
    const m = String(Math.floor(remainingSeconds / 60)).padStart(2, '0');
    const s = String(remainingSeconds % 60).padStart(2, '0');
    timerEl.textContent = `${m}:${s}`;

    if (remainingSeconds <= 0) {
      clearInterval(pvqCountdownInterval);
      alert('Verification timeout. Your course session has been paused.');
      window.location.reload();
    }
  }, 1000);

  document.getElementById('pvq-submit').onclick = async () => {
    const val = inputEl.value.trim();
    if (!val) return;

    try {
      const res = await fetch(`${API_BASE_URL}/api/v1/pvq/verify`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ questionKey: challenge.questionKey, answer: val }),
      });
      const result = await res.json();
      if (result.isCorrect) {
        clearInterval(pvqCountdownInterval);
        modal.remove();
        if (frame) frame.style.pointerEvents = 'auto';
      } else {
        alert('Incorrect answer. Please verify and try again.');
      }
    } catch (err) {
      alert('Verification network error: ' + err.message);
    }
  };
}

// Trigger Stripe Checkout
async function startStripeCheckout(tier = 'STANDARD') {
  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/billing/create-checkout-session`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ tier, clientOrigin: window.location.origin }),
    });

    const data = await res.json();
    if (data.success && data.checkoutUrl) {
      window.location.href = data.checkoutUrl;
    } else {
      alert('Checkout error: ' + (data.error || 'Could not initiate Stripe session'));
    }
  } catch (err) {
    alert('Network error connecting to Stripe: ' + err.message);
  }
}

function showPaymentBanner() {
  let banner = document.getElementById('unpaid-banner');
  if (!banner) {
    banner = document.createElement('div');
    banner.id = 'unpaid-banner';
    banner.className = 'fixed top-[64px] left-0 w-full bg-gradient-to-r from-amber-600 to-amber-700 text-white px-4 py-2 z-30 flex items-center justify-between text-xs font-mono shadow-md';
    banner.innerHTML = `
      <div class="flex items-center gap-2">
        <span class="material-symbols-outlined text-[16px]">info</span>
        <span><strong>FREE TRIAL ACTIVE:</strong> Module 1 is unlocked! Use code <strong>TEXAS100</strong> for 100% off to unlock Modules 2–9.</span>
      </div>
      <div class="flex items-center gap-2">
        <button onclick="if(window.showUnlockModal) window.showUnlockModal();" class="bg-black/40 hover:bg-black/60 text-emerald-300 border border-emerald-400/40 px-2.5 py-1 rounded text-xs font-bold uppercase transition-colors cursor-pointer">Apply Code TEXAS100 (100% OFF)</button>
        <button onclick="startStripeCheckout('STANDARD')" class="bg-white text-slate-900 hover:bg-gray-100 font-bold px-3 py-1 rounded text-xs transition-colors cursor-pointer">ENROLL ($38)</button>
      </div>
    `;
    document.body.appendChild(banner);
  }
}

function hidePaymentBanner() {
  const banner = document.getElementById('unpaid-banner');
  if (banner) banner.remove();
}

async function handleLogout() {
  try {
    await fetch(`${API_BASE_URL}/api/v1/auth/logout`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({}),
    });
  } catch (err) {}

  if (window.google && window.google.accounts && window.google.accounts.id) {
    window.google.accounts.id.disableAutoSelect();
  }

  currentUser = null;
  localStorage.clear();
  sessionStorage.clear();

  window.location.href = 'index.html';
}
window.handleLogout = handleLogout;

window.addEventListener('DOMContentLoaded', initCloudSync);
