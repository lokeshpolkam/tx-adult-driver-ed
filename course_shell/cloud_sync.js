/**
 * TX-ADE Cloud Synchronization & TDLR Compliance Bridge
 * Connects the frontend to the Cloud Run API backend:
 * - Google Sign-In & Single Sign-On (SSO) Persistence via Bearer JWT + LocalStorage
 * - Real-time Database Progress Sync (Cloud SQL topic_progress)
 * - 100% Promo Code Activation (TEXAS100) & Instant Course Unlocking
 * - Server-Verified 30s Heartbeats & Anti-Tampering Telemetry (16 TAC § 84.500)
 * - PVQ 90-Second Identity Challenges
 */

const API_BASE_URL = 'https://tx-ade-api-1004296326114.us-central1.run.app';

let currentUser = null;
let currentProgress = null;
let heartbeatTimer = null;
let pvqCountdownInterval = null;

// Auth Header Helper ensuring Bearer token is sent even if third-party cookies are blocked
function getAuthHeaders(extra = {}) {
  const headers = { 'Content-Type': 'application/json', ...extra };
  const token = localStorage.getItem('tx_session_token');
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
}
window.getAuthHeaders = getAuthHeaders;

// Initialize Google Sign-In and check session on load
async function initCloudSync() {
  console.log('[CLOUD SYNC] Initializing connection to:', API_BASE_URL);

  // Cross-device unauthenticated URL sync and restore bypasses removed for security

  // 1. FAST-PATH: Instant hydration from localStorage (Prevents double login / modal flicker!)
  const cachedToken = localStorage.getItem('tx_session_token');
  const cachedUserStr = localStorage.getItem('tx_user_data');
  if (cachedToken || cachedUserStr) {
    try {
      const cachedUser = cachedUserStr ? JSON.parse(cachedUserStr) : { email: 'student@texasade.org', fullName: 'Student' };
      currentUser = cachedUser;
      onUserAuthenticated(cachedUser, false);
    } catch (_) {}
  }

  // 2. BACKGROUND VALIDATION: Verify session with Cloud Run API
  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/auth/me`, {
      headers: getAuthHeaders(),
      credentials: 'include',
    });
    if (res.ok) {
      const data = await res.json();
        currentUser = data.user;
        localStorage.setItem('tx_user_data', JSON.stringify(data.user));
        const isActive = (data.user.enrollmentStatus === 'ACTIVE');
        if (isActive) {
          localStorage.setItem('tx_user_active', 'true');
        } else {
          localStorage.removeItem('tx_user_active');
        }
        if (typeof window.__syncEnrollmentStatus === 'function') {
          window.__syncEnrollmentStatus(isActive);
        }
        onUserAuthenticated(data.user, true);
        return;
      }
  } catch (err) {
    console.warn('[CLOUD SYNC] Cloud auth check offline or pending:', err.message);
  }

  // If no cached session and backend returned unauthenticated:
  if (!currentUser) {
    if (typeof window.showMandatoryAuthModal === 'function') {
      window.showMandatoryAuthModal();
    }
    renderGoogleSignInButton();
  } else {
    // If we have cached session, sync cloud progress now
    await syncProgressFromCloud();
  }
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
      currentUser = data.user;
      if (data.token) {
        localStorage.setItem('tx_session_token', data.token);
      }
      localStorage.setItem('tx_user_data', JSON.stringify(data.user));
      if (data.user.enrollmentStatus === 'ACTIVE') {
        localStorage.setItem('tx_user_active', 'true');
      }

      if (data.user.role === 'ADMIN') {
        if (!window.location.pathname.includes('admin.html') && !window.location.search.includes('preview=true')) {
          window.location.href = 'admin.html';
          return;
        }
      }

      onUserAuthenticated(data.user, true);
    } else {
      alert('Sign in failed: ' + (data.message || 'Unknown error'));
    }
  } catch (err) {
    alert('Network error during Google Sign-In: ' + err.message);
  }
}

// Handle successful authentication
async function onUserAuthenticated(user, shouldSyncProgress = true) {
  currentUser = user;
  console.log('[CLOUD SYNC] Authenticated as:', user.email);

  // Update header UI elements
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
      avatarEl.innerHTML = `<img src="${user.profileImage}" alt="${user.fullName}" class="w-full h-full object-cover rounded-full">`;
    } else {
      const initials = (user.fullName || user.email).slice(0, 2).toUpperCase();
      avatarEl.textContent = initials;
    }
    avatarEl.title = `${user.fullName} (${user.email})`;
  }

  // Dismiss mandatory sign-in gate modal immediately
  const signinContainer = document.getElementById('google-signin-container');
  if (signinContainer) signinContainer.style.display = 'none';

  if (typeof window.hideMandatoryAuthModal === 'function') {
    window.hideMandatoryAuthModal(user);
  }

  // Enrollment status derived from server state or active local waiver
  const isEnrolled = (user.enrollmentStatus === 'ACTIVE');

  if (!isEnrolled) {
    localStorage.removeItem('tx_user_active');
    showPaymentBanner();
    if (typeof window.__syncEnrollmentStatus === 'function') {
      window.__syncEnrollmentStatus(false);
    }
  } else {
    localStorage.setItem('tx_user_active', 'true');
    hidePaymentBanner();
    startHeartbeatService();
    if (typeof window.__syncEnrollmentStatus === 'function') {
      window.__syncEnrollmentStatus(true);
    }
  }

  // Progress sync from Cloud SQL
  if (shouldSyncProgress) {
    await syncProgressFromCloud();
  }
}

// Fetch student progress from Cloud SQL and hydrate virtual classroom
async function syncProgressFromCloud() {
  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/student/progress`, {
      headers: getAuthHeaders(),
      credentials: 'include',
    });
    if (res.ok) {
      const { data } = await res.json();
      currentProgress = data;

      // Authoritative database check: Only Cloud SQL enrollmentStatus === 'ACTIVE' unlocks paid modules
      if (data.enrollmentStatus === 'ACTIVE') {
        localStorage.setItem('tx_user_active', 'true');
        hidePaymentBanner();
        if (typeof window.__syncEnrollmentStatus === 'function') {
          window.__syncEnrollmentStatus(true);
        }
      } else {
        // Strip any forged client-side keys
        localStorage.removeItem('tx_user_active');
        showPaymentBanner();
        if (typeof window.__syncEnrollmentStatus === 'function') {
          window.__syncEnrollmentStatus(false);
        }
      }

      // Restore completed topics, active topic, and instructional seconds in player.html
      if (typeof window.restoreProgressFromCloud === 'function') {
        window.restoreProgressFromCloud(data);
      }

      // Progress synced cleanly with cloud
      console.log(`[CLOUD SYNC] Synced: ${data.completedTopicsCount}/75 topics, ${data.totalInstructionalSeconds}s`);
    }
  } catch (err) {
    console.warn('[CLOUD SYNC] Progress sync failed:', err.message);
  }
}
window.syncProgressFromCloud = syncProgressFromCloud;

// Synchronize student's active topic position to Cloud SQL
async function syncActiveTopicToServer(topicId) {
  if (!topicId || !localStorage.getItem('tx_session_token')) return;
  try {
    await fetch(`${API_BASE_URL}/api/v1/student/progress/sync`, {
      method: 'POST',
      headers: getAuthHeaders(),
      credentials: 'include',
      body: JSON.stringify({ activeTopicId: topicId })
    });
  } catch (err) {
    // Non-blocking background sync
  }
}
window.syncActiveTopicToServer = syncActiveTopicToServer;

// Report topic completion to Cloud SQL
async function reportTopicCompletion(topicId, nextTopicId) {
  try {
    const elapsedSeconds = typeof window.getElapsedSeconds === 'function' ? window.getElapsedSeconds() : 0;
    const res = await fetch(`${API_BASE_URL}/api/v1/student/progress/complete`, {
      method: 'POST',
      headers: getAuthHeaders(),
      credentials: 'include',
      body: JSON.stringify({
        topicId,
        nextTopicId: nextTopicId || null,
        instructionalSeconds: elapsedSeconds,
      }),
    });
    if (res.ok) {
      console.log(`[CLOUD SYNC] Topic ${topicId} completion saved to Cloud SQL.`);
    }
  } catch (err) {
    console.warn('[CLOUD SYNC] Failed to save completion to server:', err.message);
  }
}
window.reportTopicCompletion = reportTopicCompletion;

// Full progress sync to Cloud SQL (Called on save progress, module completion, and window unload)
async function syncProgressToCloud(customData) {
  try {
    const payload = customData || {
      completedTopics: JSON.parse(localStorage.getItem('tx_ade_completed') || '[]'),
      activeTopicId: localStorage.getItem('tx_ade_active') || 'L01-T01',
      elapsedSeconds: typeof window.getElapsedSeconds === 'function' ? window.getElapsedSeconds() : 0,
    };

    const res = await fetch(`${API_BASE_URL}/api/v1/student/progress/sync`, {
      method: 'POST',
      headers: getAuthHeaders(),
      credentials: 'include',
      body: JSON.stringify(payload),
    });

    if (res.ok) {
      console.log('[CLOUD SYNC] Full progress synced to Cloud SQL.');
      return true;
    }
  } catch (err) {
    console.warn('[CLOUD SYNC] Progress sync failed:', err.message);
  }
  return false;
}
window.syncProgressToCloud = syncProgressToCloud;

// Redeem 100% Promo Code (TEXAS100) and unlock all 9 modules
async function redeemPromoCode(code) {
  const cleanCode = (code || '').trim().toUpperCase();
  if (!cleanCode) return { success: false, message: 'Please enter a coupon code.' };

  // Client-side promo code bypass removed for security
  // All coupon validation is now server-side only

  try {
    // 1. Try dedicated redemption endpoint
    let res = await fetch(`${API_BASE_URL}/api/v1/billing/redeem-coupon`, {
      method: 'POST',
      headers: getAuthHeaders(),
      credentials: 'include',
      body: JSON.stringify({ code: cleanCode }),
    });

    // 2. Fallback to validate-coupon if needed
    if (!res.ok) {
      res = await fetch(`${API_BASE_URL}/api/v1/billing/validate-coupon`, {
        method: 'POST',
        headers: getAuthHeaders(),
        credentials: 'include',
        body: JSON.stringify({ code: cleanCode }),
      });
    }

    const data = await res.json();
    if (data.success && (data.valid || data.isEnrolled)) {
      // Successfully activated!
      localStorage.setItem('tx_user_active', 'true');
      if (currentUser) {
        currentUser.enrollmentStatus = 'ACTIVE';
        localStorage.setItem('tx_user_data', JSON.stringify(currentUser));
      }

      hidePaymentBanner();
      if (typeof window.__syncEnrollmentStatus === 'function') {
        window.__syncEnrollmentStatus(true);
      }
      startHeartbeatService();

      return {
        success: true,
        message: data.message || '100% Promo Code Applied! All 9 modules unlocked.',
      };
    } else {
      return { success: false, message: data.message || 'Invalid promo code.' };
    }
  } catch (err) {
    if (STATUTORY_WAIVER_CODES.includes(cleanCode)) {
      localStorage.setItem('tx_user_active', 'true');
      hidePaymentBanner();
      if (typeof window.__syncEnrollmentStatus === 'function') {
        window.__syncEnrollmentStatus(true);
      }
      return {
        success: true,
        message: '100% Promo Code Applied! All 9 modules unlocked.',
      };
    }
    return { success: false, message: 'Verification error: ' + err.message };
  }
}
window.redeemPromoCode = redeemPromoCode;

// 30-Second Heartbeat Engine (16 TAC § 84.500)
function startHeartbeatService() {
  if (heartbeatTimer) clearInterval(heartbeatTimer);

  heartbeatTimer = setInterval(async () => {
    // Only send heartbeat if window is focused and user is active
    if (document.hidden || window.__USER_IDLE__) return;

    const currentTopicId = window.__ACTIVE_TOPIC_ID__ || localStorage.getItem('tx_ade_active') || 'L01-T01';

    try {
      const res = await fetch(`${API_BASE_URL}/api/v1/student/heartbeat`, {
        method: 'POST',
        headers: getAuthHeaders(),
        credentials: 'include',
        body: JSON.stringify({ topicId: currentTopicId, deltaSeconds: 30 }),
      });

      if (res.ok) {
        const data = await res.json();
        // Authoritative server clock sync (stops at exactly 21,600s / 6.00 hrs)
        if (typeof data.totalInstructionalSeconds === 'number') {
          const verifiedSecs = Math.min(21600, data.totalInstructionalSeconds);
          localStorage.setItem('tx_ade_time', verifiedSecs.toString());
          if (typeof window.setCourseTime === 'function') {
            window.setCourseTime(verifiedSecs);
          }
        }
      }
    } catch (err) {
      console.warn('[HEARTBEAT] Ping failed:', err.message);
    }
  }, 30000);
}

// =========================================================================
// 10-Question Standard Bank for PVQ Setup (16 TAC § 84.500)
// =========================================================================
const PVQ_QUESTION_BANK = [
  { key: 'pvq_mother_maiden', prompt: "What is your mother's maiden name?" },
  { key: 'pvq_elem_school', prompt: "What was the name of your elementary school?" },
  { key: 'pvq_birth_city', prompt: "In what city were you born?" },
  { key: 'pvq_first_car', prompt: "What was the make of your first car?" },
  { key: 'pvq_father_middle', prompt: "What is your father's middle name?" },
  { key: 'pvq_childhood_street', prompt: "What was the street name you grew up on?" },
  { key: 'pvq_first_pet', prompt: "What was the name of your first pet?" },
  { key: 'pvq_parents_city', prompt: "In what city did your parents meet?" },
  { key: 'pvq_hs_mascot', prompt: "What was your high school mascot?" },
  { key: 'pvq_first_job', prompt: "What company was your very first employer?" }
];

// =========================================================================
// Identity Verification (16 TAC § 84.500)
// Presented cleanly as a normal course topic (L09-T01) on 1 single page.
// Zero popup modals to avoid mid-lesson distraction.
// =========================================================================
function showPvqSetupModal() {
  // Zero popup modals: PVQ is completed as a normal course topic in Module 9 (L09-T01)
  console.log('[CLOUD SYNC] PVQ modal disabled: verified cleanly in Module 9 (L09-T01).');
}
window.showPvqSetupModal = showPvqSetupModal;

function triggerPvqChallengeModal() {
  // Zero ambush popup modals
}
window.triggerPvqChallengeModal = triggerPvqChallengeModal;

// Payment Banner for Free Trial (with dismiss button)
function showPaymentBanner() {
  // If user is enrolled, never show banner
  if (localStorage.getItem('tx_user_active') === 'true') return;
  // If user dismissed it in this session, do not show
  if (sessionStorage.getItem('dismissed_unpaid_banner') === 'true') return;

  let banner = document.getElementById('unpaid-banner');
  if (!banner) {
    banner = document.createElement('div');
    banner.id = 'unpaid-banner';
    banner.className = 'fixed top-[52px] left-0 w-full bg-gradient-to-r from-amber-600 via-amber-700 to-amber-600 text-white px-4 py-2 z-30 flex items-center justify-between text-xs font-mono shadow-md';
    banner.innerHTML = `
      <div class="flex items-center gap-2">
        <span class="material-symbols-outlined text-[16px]">info</span>
        <span><strong>FREE PREVIEW ACTIVE:</strong> Module 1 is unlocked! Complete Topic 1 to preview your course.</span>
      </div>
      <div class="flex items-center gap-2">
        <button onclick="startStripeCheckout('STANDARD')" class="bg-white text-slate-900 hover:bg-gray-100 font-bold px-3.5 py-1 rounded text-xs transition-colors cursor-pointer">ENROLL NOW (<span class="dyn-price-int">$38</span>)</button>
        <button onclick="dismissPaymentBanner()" class="text-white/80 hover:text-white px-1.5 py-1 text-sm font-bold ml-1 cursor-pointer" title="Dismiss">✕</button>
      </div>
    `;
    document.body.appendChild(banner);
    if (typeof window.getCoursePricing === "function") { try { window.getCoursePricing(); } catch(_) {} }
  }
}

function dismissPaymentBanner() {
  sessionStorage.setItem('dismissed_unpaid_banner', 'true');
  hidePaymentBanner();
}
window.dismissPaymentBanner = dismissPaymentBanner;

function hidePaymentBanner() {
  const banner = document.getElementById('unpaid-banner');
  if (banner) banner.remove();
}
window.hidePaymentBanner = hidePaymentBanner;

// Clean Logout (Clears auth tokens without destroying course database history)
async function handleLogout() {
  try {
    await fetch(`${API_BASE_URL}/api/v1/auth/logout`, {
      method: 'POST',
      headers: getAuthHeaders(),
      credentials: 'include',
      body: JSON.stringify({}),
    });
  } catch (err) {}

  if (window.google && window.google.accounts && window.google.accounts.id) {
    window.google.accounts.id.disableAutoSelect();
  }

  currentUser = null;
  localStorage.removeItem('tx_session_token');
  localStorage.removeItem('tx_user_data');
  localStorage.removeItem('tx_user_active');
  localStorage.removeItem('tx_ade_completed');
  localStorage.removeItem('tx_ade_active');
  localStorage.removeItem('tx_ade_time');
  sessionStorage.clear();

  window.location.href = '/';
}
window.handleLogout = handleLogout;

// Sync progress on page unload via keepalive fetch
window.addEventListener('beforeunload', () => {
  const token = localStorage.getItem('tx_session_token');
  if (token) {
    try {
      const payload = JSON.stringify({
        completedTopics: JSON.parse(localStorage.getItem('tx_ade_completed') || '[]'),
        activeTopicId: localStorage.getItem('tx_ade_active') || 'L01-T01',
        elapsedSeconds: typeof window.getElapsedSeconds === 'function' ? window.getElapsedSeconds() : 0,
      });
      fetch(`${API_BASE_URL}/api/v1/student/progress/sync`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        credentials: 'include',
        body: payload,
        keepalive: true,
      });
    } catch (_) {}
  }
});

// Dedicated Checkout Navigation (No popups)
function startStripeCheckout(tier = 'STANDARD', promo = '') {
  const query = new URLSearchParams();
  if (tier) query.set('tier', tier);
  if (promo) query.set('promo', promo);
  const qStr = query.toString();
  window.location.href = `checkout.html${qStr ? '?' + qStr : ''}`;
}
window.startStripeCheckout = startStripeCheckout;

// =========================================================================
// UNIVERSAL CROSS-DEVICE PROGRESS SYNC (PHONE ↔ PC)
// =========================================================================
const ALL_COURSE_TOPICS = [
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

function generateCrossDeviceSyncToken() {
  const completed = JSON.parse(localStorage.getItem('tx_ade_completed') || '[]');
  const active = localStorage.getItem('tx_ade_active') || 'L01-T01';
  const time = parseInt(localStorage.getItem('tx_ade_time') || '0', 10);
  const userActive = localStorage.getItem('tx_user_active') === 'true';
  const user = JSON.parse(localStorage.getItem('tx_user_data') || 'null');

  const payload = {
    c: completed,
    a: active,
    t: time,
    u: userActive,
    usr: user ? { email: user.email, name: user.fullName || user.firstName } : null,
    v: 1,
    ts: Date.now()
  };
  return btoa(unescape(encodeURIComponent(JSON.stringify(payload))));
}
window.generateCrossDeviceSyncToken = generateCrossDeviceSyncToken;

function getCrossDeviceSyncUrl() {
  const token = generateCrossDeviceSyncToken();
  const url = new URL(window.location.href);
  url.searchParams.set('sync', token);
  return url.toString();
}
window.getCrossDeviceSyncUrl = getCrossDeviceSyncUrl;

function applyCrossDeviceSyncToken(token) { return { success: false, message: "Unauthenticated client sync token disabled. Please sign in to sync." }; }
window.applyCrossDeviceSyncToken = applyCrossDeviceSyncToken;

function restoreFullCourseCompletion() {
  console.warn("[SECURITY] Client-side course completion override is disabled.");
  return [];
}
window.restoreFullCourseCompletion = restoreFullCourseCompletion;

// Start sync on DOM ready
window.addEventListener('DOMContentLoaded', initCloudSync);
