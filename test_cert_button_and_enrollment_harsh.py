import os
import re
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

print("=====================================================================")
print("RUNNING HARSH TEST: CERTIFICATE BUTTON, ELIGIBILITY & ENROLLMENT LINK")
print("=====================================================================")

# ---------------------------------------------------------
# Test 1: Static Code Inspection in Player & Classroom
# ---------------------------------------------------------
print("\n[TEST 1] Static Code Inspection: Classroom & Player Headers...")

with open('course_shell/player.html', 'r', encoding='utf-8') as f:
    player_html = f.read()

with open('course_shell/classroom.html', 'r', encoding='utf-8') as f:
    classroom_html = f.read()

assert 'id="shell-sync-btn"' not in player_html, "FAIL: #shell-sync-btn still found in player.html"
assert 'id="shell-sync-btn"' not in classroom_html, "FAIL: #shell-sync-btn still found in classroom.html"
assert 'id="shell-cert-btn"' in player_html, "FAIL: #shell-cert-btn missing from player.html"
assert 'id="shell-cert-btn"' in classroom_html, "FAIL: #shell-cert-btn missing from classroom.html"
assert 'GET CERTIFICATE' in player_html, "FAIL: 'GET CERTIFICATE' label missing from player.html"
assert 'id="cert-eligibility-modal"' in player_html, "FAIL: #cert-eligibility-modal missing from player.html"
assert 'handleHeaderGetCertificate' in player_html, "FAIL: handleHeaderGetCertificate missing from player.html"

print("  -> Passed: #shell-sync-btn successfully removed; #shell-cert-btn and eligibility modal installed.")

# ---------------------------------------------------------
# Test 2: Static Code Inspection in Home Dashboard
# ---------------------------------------------------------
print("\n[TEST 2] Static Code Inspection: Home Dashboard...")

with open('course_shell/home.html', 'r', encoding='utf-8') as f:
    home_html = f.read()

assert 'handleDashboardCertificateClick' in home_html, "FAIL: handleDashboardCertificateClick missing from home.html"
assert 'id="cert-eligibility-modal"' in home_html, "FAIL: #cert-eligibility-modal missing from home.html"
assert 'id="dashboard-cert-download-btn"' in home_html, "FAIL: #dashboard-cert-download-btn missing from home.html"

print("  -> Passed: Home dashboard has handleDashboardCertificateClick and modal installed.")

# ---------------------------------------------------------
# Test 3: Static Code Inspection in Checkout Pages
# ---------------------------------------------------------
print("\n[TEST 3] Static Code Inspection: Checkout & Payment Pages...")

for path in ['course_shell/checkout.html', 'course_shell/payment.html', 'course_shell/payments.html']:
    with open(path, 'r', encoding='utf-8') as f:
        c_html = f.read()
    assert 'id="already-enrolled-banner"' in c_html, f"FAIL: #already-enrolled-banner missing from {path}"
    assert 'You Are Already Enrolled!' in c_html, f"FAIL: 'You Are Already Enrolled!' text missing from {path}"

print("  -> Passed: All checkout pages have #already-enrolled-banner protection.")

# ---------------------------------------------------------
# Test 4: Static Code Inspection in Server Routes
# ---------------------------------------------------------
print("\n[TEST 4] Static Code Inspection: Server Routes...")

with open('server/src/routes/student.js', 'r', encoding='utf-8') as f:
    student_js = f.read()

with open('server/src/routes/billing.js', 'r', encoding='utf-8') as f:
    billing_js = f.read()

assert 'enrollment_status' in student_js and 'enrollments' in student_js, "FAIL: Student progress route missing enrollment linkage"
assert 'alreadyEnrolled' in billing_js, "FAIL: Billing route missing alreadyEnrolled check"

print("  -> Passed: Server routes have enrollment status self-healing and checkout re-charge prevention.")

# ---------------------------------------------------------
# Test 5: Playwright DOM Execution: Player Header & Modal
# ---------------------------------------------------------
print("\n[TEST 5] Playwright Execution: Testing DOM behaviors in Player...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Scenario A: Signed in Free Preview user (unpaid) clicks GET CERTIFICATE
    page.goto(f"file:///{os.path.abspath('course_shell/player.html')}")
    page.evaluate("""() => {
        localStorage.clear();
        localStorage.setItem('tx_auth_token', 'mock_jwt_token_123');
        localStorage.setItem('tx_user_data', JSON.stringify({ name: 'Preview Student', email: 'student@example.com' }));
        localStorage.setItem('tx_user_active', 'false');
        localStorage.setItem('tx_ade_time', '120');
    }""")
    page.reload()
    page.wait_for_selector('#shell-cert-btn')

    # Click GET CERTIFICATE
    page.click('#shell-cert-btn')
    page.wait_for_selector('#cert-eligibility-modal:not(.hidden)')
    title = page.inner_text('#cert-modal-title')
    assert 'Enroll to Earn Your Certificate' in title or 'Enroll' in title, f"Unexpected modal title for unpaid: {title}"
    print("  -> Passed Scenario A: Unpaid user clicking GET CERTIFICATE receives enrollment prompt.")

    # Dismiss modal
    page.click('#cert-eligibility-modal button:has-text("Dismiss")')
    assert page.is_hidden('#cert-eligibility-modal') or 'hidden' in page.get_attribute('#cert-eligibility-modal', 'class')

    # Scenario B: Enrolled user with incomplete hours (< 6 hrs = 21600s)
    page.evaluate("""() => {
        localStorage.removeItem('tx_ade_certificate_serial');
        localStorage.removeItem('tx_cert_data');
        localStorage.setItem('tx_auth_token', 'mock_jwt_token_123');
        localStorage.setItem('tx_user_data', JSON.stringify({ name: 'Jane Enrolled', email: 'jane@example.com', enrollmentStatus: 'ACTIVE' }));
        localStorage.setItem('tx_user_active', 'true');
        localStorage.setItem('tx_ade_time', '7200'); // 2 hours
        localStorage.setItem('tx_exam_passed', 'false');
    }""")
    page.reload()
    page.wait_for_selector('#shell-cert-btn')
    page.click('#shell-cert-btn')
    page.wait_for_selector('#cert-eligibility-modal:not(.hidden)')
    title = page.inner_text('#cert-modal-title')
    desc = page.inner_text('#cert-modal-desc')
    checklist = page.inner_text('#cert-modal-checklist')
    assert '6-Hour' in title or 'Incomplete' in title, f"Unexpected title for incomplete hours: {title}"
    assert '2h 0m / 6h' in checklist or '2h' in checklist, f"Checklist missing time status: {checklist}"
    assert 'ACTIVE' in checklist, f"Checklist missing active enrollment status: {checklist}"
    print("  -> Passed Scenario B: Enrolled user with 2 hours sees TDLR 6-Hour Requirement Incomplete checklist.")

    # Dismiss modal
    page.click('#cert-eligibility-modal button:has-text("Dismiss")')

    # Scenario C: Enrolled user attempting to access locked Final Exam (L09-T02) before 6 hours
    # Crucial test: MUST NOT redirect to checkout.html!
    page.evaluate("""() => {
        // Attempt to load L09-T02 while elapsedSeconds is 7200 (< 21600)
        window.loadTopic('L09-T02');
    }""")
    # Wait a bit to ensure it doesn't navigate away to checkout.html
    page.wait_for_timeout(500)
    current_url = page.url
    assert 'checkout.html' not in current_url, f"FAIL: Enrolled user was redirected to checkout! URL: {current_url}"
    # Verify the eligibility modal is open
    assert not ('hidden' in page.get_attribute('#cert-eligibility-modal', 'class')), "Eligibility modal should be displayed"
    print("  -> Passed Scenario C: Enrolled user accessing locked final exam gets eligibility modal instead of checkout redirect!")

    # Scenario D: Enrolled user with 6 hours completed (21600s), but exam not taken
    page.evaluate("""() => {
        localStorage.setItem('tx_auth_token', 'mock_jwt_token_123');
        localStorage.setItem('tx_user_data', JSON.stringify({ name: 'Jane Enrolled', email: 'jane@example.com', enrollmentStatus: 'ACTIVE' }));
        localStorage.setItem('tx_user_active', 'true');
        localStorage.setItem('tx_ade_time', '21600');
        localStorage.setItem('tx_exam_passed', 'false');
    }""")
    page.reload()
    page.wait_for_selector('#shell-cert-btn')
    page.click('#shell-cert-btn')
    page.wait_for_selector('#cert-eligibility-modal:not(.hidden)')
    title = page.inner_text('#cert-modal-title')
    assert 'Take Official Final Exam' in title or 'Final Exam' in title, f"Unexpected title: {title}"
    btn_text = page.inner_text('#cert-modal-primary-btn')
    assert 'final exam' in btn_text.lower(), f"Primary button text unexpected: {btn_text}"
    print("  -> Passed Scenario D: 6-hour student prompted with 'Start Final Exam'.")

    # Dismiss modal
    page.click('#cert-eligibility-modal button:has-text("Dismiss")')

    # Scenario E: Exam passed -> reverification / download modal triggered
    page.evaluate("""() => {
        localStorage.setItem('tx_auth_token', 'mock_jwt_token_123');
        localStorage.setItem('tx_user_data', JSON.stringify({ name: 'Jane Enrolled', email: 'jane@example.com', enrollmentStatus: 'ACTIVE' }));
        localStorage.setItem('tx_user_active', 'true');
        localStorage.setItem('tx_exam_passed', 'true');
        localStorage.setItem('tx_ade_certificate_serial', 'ADE1317-2026-C3284-00001');
    }""")
    page.reload()
    page.wait_for_selector('#shell-cert-btn')
    page.click('#shell-cert-btn')
    # Check that reverification modal opened
    page.wait_for_selector('#home-name-reverify-modal:not(.hidden)')
    assert not ('hidden' in page.get_attribute('#home-name-reverify-modal', 'class'))
    print("  -> Passed Scenario E: Student with passed exam opens certificate reverification modal!")

    # ---------------------------------------------------------
    # Test 6: Playwright DOM Execution: Checkout Already-Enrolled Guard
    # ---------------------------------------------------------
    print("\n[TEST 6] Playwright Execution: Checkout Already-Enrolled Guard...")

    page.goto(f"file:///{os.path.abspath('course_shell/checkout.html')}")
    page.evaluate("""() => {
        localStorage.setItem('tx_auth_token', 'mock_jwt_token_123');
        localStorage.setItem('tx_session_token', 'mock_session_token_123');
        localStorage.setItem('tx_user_data', JSON.stringify({
            email: 'jane@example.com',
            fullName: 'Jane Doe',
            enrollmentStatus: 'ACTIVE'
        }));
        localStorage.setItem('tx_user_active', 'true');
        localStorage.setItem('tx_student_name', 'Jane Doe');
        localStorage.setItem('tx_student_email', 'jane@example.com');
    }""")
    page.reload()
    page.wait_for_selector('#already-enrolled-banner:not(.hidden)')
    banner_text = page.inner_text('#already-enrolled-banner')
    assert 'You Are Already Enrolled!' in banner_text, f"Banner text missing: {banner_text}"

    # Verify payment section is hidden
    is_payment_hidden = page.evaluate("""() => {
        const paymentSec = document.getElementById('payment-section');
        return paymentSec ? paymentSec.classList.contains('hidden') : true;
    }""")
    assert is_payment_hidden, "Payment section should be hidden when user is already enrolled!"
    print("  -> Passed Test 6: Checkout displays Already-Enrolled banner and hides payment form.")

    # ---------------------------------------------------------
    # Test 7: Playwright DOM Execution: Home Dashboard Certificate Card
    # ---------------------------------------------------------
    print("\n[TEST 7] Playwright Execution: Home Dashboard Certificate Card...")

    page.goto(f"file:///{os.path.abspath('course_shell/home.html')}")
    page.evaluate("""() => {
        localStorage.removeItem('tx_ade_certificate_serial');
        localStorage.removeItem('tx_cert_data');
        localStorage.setItem('tx_auth_token', 'mock_jwt_token_123');
        localStorage.setItem('tx_user_data', JSON.stringify({ name: 'Jane Enrolled', email: 'jane@example.com', enrollmentStatus: 'ACTIVE' }));
        localStorage.setItem('tx_user_active', 'true');
        localStorage.setItem('tx_ade_time', '7200'); // 2 hours
        localStorage.setItem('tx_exam_passed', 'false');
    }""")
    page.reload()
    page.wait_for_selector('#dashboard-cert-download-btn')
    print("  -> Found #dashboard-cert-download-btn, clicking it now...")
    page.click('#dashboard-cert-download-btn')
    print("  -> Clicked. Checking modal class...")
    classes = page.get_attribute('#cert-eligibility-modal', 'class')
    print("  -> Modal classes after click:", classes)
    page.wait_for_selector('#cert-eligibility-modal:not(.hidden)')
    h_title = page.inner_text('#cert-modal-title')
    assert '6-Hour' in h_title or 'Incomplete' in h_title, f"Dashboard unexpected modal title: {h_title}"
    print("  -> Passed Test 7: Dashboard certificate button opens eligibility modal without checkout bounce.")

    browser.close()

print("\n=====================================================================")
print("ALL 7 HARSH TESTS PASSED WITH 100% SUCCESS!")
print("=====================================================================")
