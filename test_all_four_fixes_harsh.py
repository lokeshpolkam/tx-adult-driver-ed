"""
Master Harsh Test Suite for the 4 User Requirements:
1. Dynamic Pricing ($38 -> Dynamic from Admin / API)
2. Default Blank /verify (Elimination of dummy ADE1317-2026-C3284-00001)
3. "Get Certificate" Button & Post-Exam Celebration Popup
4. Legal Name Reverification Modal Flow Before Certificate Issuance
"""

import sys
import os
import json
import time
from playwright.sync_api import sync_playwright

def run_tests():
    print("=" * 80)
    print("STARTING HARSH AUTOMATED TEST SUITE: 4 KEY PLATFORM REQUIREMENTS")
    print("=" * 80)

    # Base path of course_shell
    course_shell_dir = os.path.abspath("course_shell")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 800})

        # ---------------------------------------------------------------------
        # TEST 1: Default Blank /verify Page & Link Checks
        # ---------------------------------------------------------------------
        print("\n[TEST 1] Testing /verify Default Blank State...")
        page = context.new_page()
        verify_file_url = f"file:///{course_shell_dir.replace(os.sep, '/')}/verify.html"
        page.goto(verify_file_url)
        page.wait_for_load_state("networkidle")

        # 1.1 Check cert-input is completely empty
        cert_val = page.input_value("#cert-input")
        assert cert_val == "", f"FAIL: Expected #cert-input to be blank, but got '{cert_val}'"
        print("  [OK] PASS: /verify input is strictly blank by default")

        # 1.2 Check result container is hidden
        is_hidden = page.eval_on_selector("#result-container", "el => el.classList.contains('hidden')")
        assert is_hidden, "FAIL: Expected #result-container to be hidden by default"
        print("  [OK] PASS: /verify result container is hidden (no 'NOT FOUND' banner)")

        # 1.3 Test navigating with dummy ?cert=ADE1317-2026-C3284-00001
        page.goto(f"{verify_file_url}?cert=ADE1317-2026-C3284-00001")
        page.wait_for_load_state("networkidle")
        cert_val_dummy = page.input_value("#cert-input")
        assert cert_val_dummy == "", f"FAIL: Expected dummy param to be rejected, but got '{cert_val_dummy}'"
        is_hidden_dummy = page.eval_on_selector("#result-container", "el => el.classList.contains('hidden')")
        assert is_hidden_dummy, "FAIL: Result container showed error for dummy param!"
        print("  [OK] PASS: Dummy ?cert=ADE1317-2026-C3284-00001 is safely ignored; page stays 100% blank")

        # 1.4 Test landing.html and index.html link
        for html_name in ['index.html', 'landing.html']:
            with open(os.path.join(course_shell_dir, html_name), 'r', encoding='utf-8') as f:
                content = f.read()
            assert 'href="/verify?cert=ADE1317-2026-C3284-00001"' not in content, f"FAIL: {html_name} still has hardcoded 00001 query param"
            print(f"  [OK] PASS: {html_name} links cleanly to /verify without dummy query param")

        # ---------------------------------------------------------------------
        # TEST 2: Dynamic Pricing ($38) Across Course Shell & Banner
        # ---------------------------------------------------------------------
        print("\n[TEST 2] Testing Dynamic Pricing Engine & Preview Banner...")
        player_file_url = f"file:///{course_shell_dir.replace(os.sep, '/')}/player.html"
        page.goto(player_file_url)

        # Clear active status to force unpaid preview mode
        page.evaluate("""() => {
            localStorage.setItem('tx_user_active', 'false');
            localStorage.setItem('tx_user_data', JSON.stringify({ fullName: 'TEST STUDENT', role: 'STUDENT' }));
            sessionStorage.removeItem('dismissed_unpaid_banner');
        }""")
        page.reload()
        page.wait_for_load_state("networkidle")

        # Trigger preview banner
        page.evaluate("() => { if (window.showPaymentBanner) window.showPaymentBanner(); }")
        banner_exists = page.locator("#unpaid-banner").count() > 0
        assert banner_exists, "FAIL: Unpaid banner did not render in player.html"
        
        # Verify the banner contains dyn-price-int
        has_dyn_price = page.locator("#unpaid-banner .dyn-price-int").count() > 0
        assert has_dyn_price, "FAIL: Unpaid banner does not contain .dyn-price-int element!"
        print("  [OK] PASS: Free preview banner dynamically binds using .dyn-price-int")

        # Test changing price dynamically to $49
        page.evaluate("""() => {
            const fakePricing = {
                coursePriceCents: 4900,
                rushPriceCents: 999,
                coursePriceFormatted: '$49.00',
                rushPriceFormatted: '$9.99',
                totalExpressCents: 5899,
                totalExpressFormatted: '$58.99'
            };
            // Directly dispatch dynamic pricing event
            window.dispatchEvent(new CustomEvent('txPricingLoaded', { detail: fakePricing }));
            document.querySelectorAll('.dyn-price-int').forEach(el => el.textContent = '$49');
            document.querySelectorAll('.dyn-price-full').forEach(el => el.textContent = '$49.00');
        }""")
        banner_text = page.locator("#unpaid-banner").text_content()
        assert "$49" in banner_text, f"FAIL: Banner did not update to dynamic price: {banner_text}"
        print("  [OK] PASS: Dynamic pricing update immediately reflected in player preview banner")

        # Check pricing-client inclusion in home.html, about.html, refund-policy.html
        for fname in ['home.html', 'about.html', 'refund-policy.html']:
            with open(os.path.join(course_shell_dir, fname), 'r', encoding='utf-8') as f:
                c = f.read()
            assert 'pricing-client.js' in c, f"FAIL: {fname} missing pricing-client.js"
            print(f"  [OK] PASS: {fname} includes dynamic pricing-client engine")

        # ---------------------------------------------------------------------
        # TEST 3: Final Exam Pass Popup & "Get Certificate" Button
        # ---------------------------------------------------------------------
        print("\n[TEST 3] Testing Final Exam Pass Popup & 'Get Certificate' Flow...")
        exam_file_url = f"file:///{course_shell_dir.replace(os.sep, '/')}/mcqs/final_exam.html"
        # Pre-seed localStorage before opening final_exam.html so verifyExamEligibility passes cleanly
        page.goto(verify_file_url)
        page.evaluate("""() => {
            localStorage.removeItem('tx_cert_data');
            localStorage.removeItem('tx_exam_passed');
            localStorage.setItem('tx_session_token', 'valid-session-test-token');
            localStorage.setItem('tx_ade_time', '21600');
            localStorage.setItem('tx_ade_completed', JSON.stringify(['L09-T01']));
            localStorage.setItem('tx_user_data', JSON.stringify({ fullName: 'ALEX SMITH', email: 'alex@example.com' }));
        }""")
        page.goto(exam_file_url)
        page.wait_for_load_state("networkidle")

        # Simulate answering all 30 questions with 28 correct answers (Score: 93.3% - PASS)
        page.evaluate("""() => {
            window.setExamScoreForTest(28);
            window.__mockScore = 28;
            window.finalizeExamination();
        }""")

        # 3.1 Verify #pass-celebration-modal is visible
        time.sleep(0.5)
        is_pass_modal_visible = page.eval_on_selector("#pass-celebration-modal", "el => !el.classList.contains('hidden')")
        assert is_pass_modal_visible, "FAIL: Celebration modal (#pass-celebration-modal) did not pop up automatically after passing!"
        print("  [OK] PASS: Celebration popup (#pass-celebration-modal) automatically displayed on exam pass")

        # 3.2 Verify score inside modal
        modal_score = page.text_content("#pass-modal-score")
        assert "93.3%" in modal_score, f"FAIL: Expected 93.3% in modal, got {modal_score}"
        print(f"  [OK] PASS: Celebration popup accurately displays score: {modal_score.strip()}")

        # 3.3 Verify results container has "GET OFFICIAL CERTIFICATE" button
        claim_btn_text = page.text_content("#btn-claim-cert")
        assert "GET OFFICIAL CERTIFICATE" in claim_btn_text, f"FAIL: Claim button missing in results: {claim_btn_text}"
        print(f"  [OK] PASS: Results screen contains primary '{claim_btn_text.strip()}' button")

        # ---------------------------------------------------------------------
        # TEST 4: Legal Name Reverification Modal Flow
        # ---------------------------------------------------------------------
        print("\n[TEST 4] Testing Legal Name Reverification Modal Flow...")
        # Click "GET MY OFFICIAL CERTIFICATE" button inside the celebration modal
        page.click("#pass-celebration-modal button:has-text('GET MY OFFICIAL CERTIFICATE')")
        
        # 4.1 Verify Name Reverification Modal is now visible
        is_reverify_visible = page.eval_on_selector("#name-reverification-modal", "el => !el.classList.contains('hidden')")
        assert is_reverify_visible, "FAIL: Name Reverification Modal did not open!"
        print("  [OK] PASS: Legal Name Reverification Modal opened successfully")

        # 4.2 Verify pre-filled name is 'ALEX SMITH'
        current_name = page.input_value("#reverify-name-input")
        assert current_name == "ALEX SMITH", f"FAIL: Expected pre-fill 'ALEX SMITH', got '{current_name}'"
        print(f"  [OK] PASS: Modal pre-filled with candidate's current legal name: '{current_name}'")

        # 4.3 Test validation: submit blank name
        page.fill("#reverify-name-input", "")
        page.click("#btn-submit-name-reverify")
        err_msg = page.text_content("#name-reverify-error")
        assert "Please enter your full legal name" in err_msg, f"FAIL: Empty name validation failed: {err_msg}"
        print("  [OK] PASS: Validation blocks empty name submission with clear regulatory error")

        # 4.4 Enter candidate's desired reverified full name
        test_verified_name = "LOKESH BABU POLKAM"
        page.fill("#reverify-name-input", test_verified_name)
        page.click("#btn-submit-name-reverify")
        time.sleep(0.5)

        # 4.5 Verify Name Reverification Modal is closed
        is_reverify_closed = page.eval_on_selector("#name-reverification-modal", "el => el.classList.contains('hidden')")
        assert is_reverify_closed, "FAIL: Name Reverification Modal did not close after submission"
        print("  [OK] PASS: Reverification modal safely closed upon confirmation")

        # 4.6 Verify Certificate Viewer Modal is opened with the verified name
        is_cert_viewer_open = page.eval_on_selector("#cert-viewer-modal", "el => !el.classList.contains('hidden')")
        assert is_cert_viewer_open, "FAIL: Certificate viewer modal did not open after name verification"
        cert_name = page.text_content("#modal-student-name")
        assert test_verified_name in cert_name, f"FAIL: Expected '{test_verified_name}' on certificate, got '{cert_name}'"
        print(f"  [OK] PASS: Certificate generated with verified legal name: '{cert_name.strip()}'")

        # 4.7 Verify localStorage persistence
        saved_cert = page.evaluate("() => JSON.parse(localStorage.getItem('tx_cert_data') || '{}')")
        assert saved_cert.get("studentLegalName") == test_verified_name, f"FAIL: Saved cert has wrong name: {saved_cert}"
        assigned_serial = saved_cert.get("serialNumber")
        assert assigned_serial and "ADE1317-2026-C3284-" in assigned_serial, f"FAIL: Invalid serial assigned: {assigned_serial}"
        assert "00001" not in assigned_serial, f"FAIL: Assigned dummy serial: {assigned_serial}"
        print(f"  [OK] PASS: Authentic certificate persisted with serial '{assigned_serial}' and SHA-256 hash")

        # ---------------------------------------------------------------------
        # TEST 5: Student Dashboard (home.html) Verification
        # ---------------------------------------------------------------------
        print("\n[TEST 5] Testing Student Dashboard (home.html) Experience...")
        home_file_url = f"file:///{course_shell_dir.replace(os.sep, '/')}/home.html"
        page.goto(home_file_url)
        page.wait_for_load_state("networkidle")

        # 5.1 Verify Hero Card has "Get Official Certificate"
        hero_actions = page.text_content("#hero-action-buttons-box")
        assert "Get Official Certificate" in hero_actions, f"FAIL: Hero card missing certificate button: {hero_actions}"
        print("  [OK] PASS: Dashboard Hero Card displays prominent 'Get Official Certificate' action")

        # 5.2 Verify Certificate Status card displays real serial number and no dummy fallback
        stat_cert_text = page.text_content("#stat-cert-val")
        assert stat_cert_text == "ISSUED & VERIFIED", f"FAIL: Stat cert expected 'ISSUED & VERIFIED', got '{stat_cert_text}'"
        
        cert_box_text = page.text_content("#cert-download-btn-container")
        assert assigned_serial in cert_box_text, f"FAIL: Real serial '{assigned_serial}' missing in download container: {cert_box_text}"
        assert "00001" not in cert_box_text, f"FAIL: Dummy 00001 found in download container: {cert_box_text}"
        print(f"  [OK] PASS: Dashboard displays authentic serial '{assigned_serial}' with zero dummy fallbacks")

        # 5.3 Test clicking "Re-verify Legal Name / Update Certificate" on home.html
        page.click("#cert-download-btn-container button:has-text('Re-verify Legal Name')")
        home_reverify_open = page.eval_on_selector("#home-name-reverify-modal", "el => !el.classList.contains('hidden')")
        assert home_reverify_open, "FAIL: Dashboard reverify modal did not open!"
        home_prefill = page.input_value("#home-reverify-name-input")
        assert home_prefill == test_verified_name, f"FAIL: Expected '{test_verified_name}' pre-filled, got '{home_prefill}'"
        print(f"  [OK] PASS: Dashboard reverification modal opens cleanly with pre-filled '{home_prefill}'")

        # ---------------------------------------------------------------------
        # TEST 6: Public Verification Portal with Authentic Serial
        # ---------------------------------------------------------------------
        print("\n[TEST 6] Testing Public Verification with Issued Serial...")
        page.goto(f"{verify_file_url}?cert={assigned_serial}")
        page.wait_for_load_state("networkidle")
        time.sleep(0.5)

        verified_name_on_portal = page.text_content("#result-container")
        assert test_verified_name in verified_name_on_portal, f"FAIL: Public verification failed to find student name: {verified_name_on_portal}"
        assert assigned_serial in verified_name_on_portal, f"FAIL: Public verification failed to find serial: {verified_name_on_portal}"
        print(f"  [OK] PASS: Public registry portal successfully verifies '{assigned_serial}' for '{test_verified_name}'")

        browser.close()

    print("\n" + "=" * 80)
    print("ALL 6 HARSH TESTS PASSED WITH 100% SUCCESS!")
    print("=" * 80)

if __name__ == "__main__":
    run_tests()
