/**
 * Anti-Tampering & DevTools Hardening Injection for Lesson Pages
 * Enforces TDLR compliance by preventing content scraping, keyboard bypasses,
 * and reporting DevTools opening to the parent course shell.
 */
function generateAntiTamperScript(studentSession) {
  const sessionJson = JSON.stringify({
    userId: studentSession.userId,
    topicId: studentSession.topicId,
    nonce: studentSession.nonce,
  });

  return `
<style>
  /* Prevent text highlighting and copying */
  body, html {
    -webkit-user-select: none !important;
    -moz-user-select: none !important;
    -ms-user-select: none !important;
    user-select: none !important;
  }
  /* Prevent printing */
  @media print {
    body { display: none !important; }
  }
</style>
<script>
(function() {
  window.__TX_STUDENT_SESSION__ = ${sessionJson};

  // 1. Disable Right-Click Context Menu
  document.addEventListener('contextmenu', function(e) {
    e.preventDefault();
    return false;
  }, { capture: true });

  // 2. Disable Selection and Dragging
  document.addEventListener('selectstart', function(e) {
    e.preventDefault();
    return false;
  }, { capture: true });

  document.addEventListener('dragstart', function(e) {
    e.preventDefault();
    return false;
  }, { capture: true });

  // 3. Block Developer Tools & Inspection Shortcut Keys
  document.addEventListener('keydown', function(e) {
    // F12 key
    if (e.key === 'F12' || e.keyCode === 123) {
      e.preventDefault();
      e.stopPropagation();
      notifyDevToolsOpen();
      return false;
    }

    // Ctrl+Shift+I (Inspect), Ctrl+Shift+J (Console), Ctrl+Shift+C (Element picker)
    if ((e.ctrlKey || e.metaKey) && e.shiftKey) {
      const k = (e.key || '').toUpperCase();
      if (['I', 'J', 'C'].includes(k) || [73, 74, 67].includes(e.keyCode)) {
        e.preventDefault();
        e.stopPropagation();
        notifyDevToolsOpen();
        return false;
      }
    }

    // Ctrl+U (View Source), Ctrl+S (Save Page), Ctrl+P (Print)
    if (e.ctrlKey || e.metaKey) {
      const k = (e.key || '').toLowerCase();
      if (['u', 's', 'p'].includes(k)) {
        e.preventDefault();
        e.stopPropagation();
        return false;
      }
    }
  }, { capture: true });

  // 4. DevTools Geometry Heuristic & Debugger Timing Check
  let devToolsAlertSent = false;
  function notifyDevToolsOpen() {
    if (!devToolsAlertSent) {
      devToolsAlertSent = true;
      try {
        window.parent.postMessage({ type: 'DEVTOOLS_DETECTED', topicId: window.__TX_STUDENT_SESSION__.topicId }, '*');
      } catch (err) {}
    }
  }

  setInterval(function() {
    // Check viewport differential (docked DevTools causes large delta)
    const widthDiff = window.outerWidth - window.innerWidth;
    const heightDiff = window.outerHeight - window.innerHeight;
    if (widthDiff > 160 || heightDiff > 160) {
      notifyDevToolsOpen();
    }

    // Check debugger timing (if DevTools breakpoint is active)
    const start = performance.now();
    /* eslint-disable no-debugger */
    // debugger;
    const end = performance.now();
    if (end - start > 100) {
      notifyDevToolsOpen();
    }
  }, 1500);

  // 5. Signal lesson completion to parent shell when user completes interaction
  window.signalTopicCompletion = function() {
    window.parent.postMessage({
      type: 'TOPIC_COMPLETE',
      topicId: window.__TX_STUDENT_SESSION__.topicId,
      userId: window.__TX_STUDENT_SESSION__.userId
    }, '*');
  };
})();
</script>
`;
}

module.exports = { generateAntiTamperScript };
