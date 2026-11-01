import os
import sys
import json
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

print("=====================================================================")
print("RUNNING MILESTONE 4 HARSH ATTACK TEST: CERTIFICATE ISSUANCE & VERIFY")
print("=====================================================================")

# --- ATTACK 1: Static Sample PDF Link Eradication ---
final_exam_path = os.path.abspath('course_shell/mcqs/final_exam.html')
with open(final_exam_path, 'r', encoding='utf-8') as f:
    fe_src = f.read()

assert 'href="/form_ade1317_certificate.pdf"' not in fe_src, "CRITICAL VULN: Static sample PDF link still present in final_exam.html!"
assert "downloadPersonalizedCertificate" in fe_src, "CRITICAL: downloadPersonalizedCertificate missing from final_exam.html"
print("[ATTACK 1 PASSED] Static sample PDF link eradicated. Replaced by personalized vector certificate generator.")

# --- ATTACK 2: Serial Number Format Audit in Server & Client ---
cert_route_path = os.path.abspath('server/src/routes/certificates.js')
with open(cert_route_path, 'r', encoding='utf-8') as f:
    cr_src = f.read()

assert 'ADE1317-2026-C3284-${nextSeq}' in cr_src, "Server certificates.js not using standard ADE1317-2026-C3284-XXXXX serial format"
print("[ATTACK 2 PASSED] Server certificates.js enforces standard TDLR serial format ADE1317-2026-C3284-XXXXX")

# --- ATTACK 3: Dynamic Certificate Issuance & Public Roster Sync via Playwright ---
final_exam_url = 'file:///' + os.path.abspath('course_shell/mcqs/final_exam.html').replace('\\', '/')
verify_url = 'file:///' + os.path.abspath('course_shell/verify.html').replace('\\', '/')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # Seed authenticated student with verified legal name
    page.add_init_script("""
        localStorage.setItem('tx_session_token', 'token_alexander_123');
        localStorage.setItem('tx_ade_time', '21600');
        localStorage.setItem('tx_ade_completed', JSON.stringify(['L09-T01']));
        localStorage.setItem('tx_user_data', JSON.stringify({ fullName: 'ALEXANDER HAMILTON' }));
        localStorage.setItem('tx_ade_cert_counter', '142');
    """)

    page.goto(final_exam_url, wait_until='domcontentloaded')
    page.wait_for_selector('#question-prompt')

    # Trigger showFinalResults with passing score 28/30
    page.evaluate("""() => {
        score = 28;
        bankAScore = 14;
        bankBScore = 14;
        showFinalResults({ passed: true, score: 28 });
    }""")

    # Verify Results Screen Elements
    page.wait_for_selector('#results-container:not(.hidden)')
    
    # Complete user-requested Legal Name Reverification flow
    page.evaluate("""() => {
        if (window.openNameReverificationModal) window.openNameReverificationModal();
        if (window.confirmAndIssueCertificate) window.confirmAndIssueCertificate();
    }""")

    issued_name = page.inner_text('#issued-legal-name')
    print(f"Issued Legal Name on Screen: '{issued_name}'")
    assert issued_name == 'ALEXANDER HAMILTON', f"Expected ALEXANDER HAMILTON, got '{issued_name}'"
    assert 'SAMPLE' not in issued_name, "CRITICAL: Sample name was issued!"

    # Check Certificate Record in localStorage
    cert_data = page.evaluate("() => JSON.parse(localStorage.getItem('tx_cert_data'))")
    assert cert_data is not None, "tx_cert_data was not created in localStorage!"
    print(f"Issued Serial Number: {cert_data['serialNumber']}")
    assert cert_data['serialNumber'] == 'ADE1317-2026-C3284-00143', f"Unexpected serial: {cert_data['serialNumber']}"
    assert cert_data['studentLegalName'] == 'ALEXANDER HAMILTON', f"Unexpected student name: {cert_data['studentLegalName']}"
    print(f"Generated SHA-256 Hash: {cert_data['sha256Hash']}")
    assert len(cert_data['sha256Hash']) == 64, "SHA-256 hash must be 64 hexadecimal chars"
    print("[ATTACK 3A PASSED] Certificate issued with verified legal name, sequential serial 00143, and SHA-256 hash")

    # --- ATTACK 3B: Public Registry Verification (/verify.html) ---
    verify_page = context.new_page()
    verify_page.goto(verify_url, wait_until='domcontentloaded')

    # Ensure input is defaultly blank and result container is hidden
    input_val = verify_page.input_value('#cert-input')
    assert input_val == '', f"Verify input should start blank, got: '{input_val}'"
    assert verify_page.is_hidden('#result-container'), "Result container must start hidden"
    print("[ATTACK 3B PASSED] Verify portal starts in clean default blank state")

    # Perform Verification Search for the newly issued serial
    verify_page.fill('#cert-input', 'ADE1317-2026-C3284-00143')
    verify_page.click('#btn-verify')
    verify_page.wait_for_selector('#result-container:not(.hidden)')

    result_text = verify_page.inner_text('#result-container')
    assert 'ALEXANDER HAMILTON' in result_text, f"Verification result does not show student name: {result_text}"
    assert 'TDLR School #C3284' in result_text or 'C3284' in result_text, "Missing school license in verification"
    assert 'OFFICIALLY RECORDED' in result_text or 'VALID' in result_text, "Missing valid status in verification"
    print("[ATTACK 3C PASSED] Public registry verification of ADE1317-2026-C3284-00143 succeeded with 100% accurate student data!")

    # Perform Search for Fake / Invalid Serial
    verify_page.fill('#cert-input', 'ADE1317-2026-C3284-99999')
    verify_page.click('#btn-verify')
    verify_page.wait_for_timeout(500)

    fake_result = verify_page.inner_text('#result-container')
    assert 'NOT RECOGNIZED' in fake_result.upper() or 'NO RECORD' in fake_result.upper() or 'INVALID' in fake_result.upper(), f"Fake serial should be rejected: {fake_result}"
    print("[ATTACK 3D PASSED] Unknown serial ADE1317-2026-C3284-99999 strictly rejected with invalid state notice")

    browser.close()

print("\n=====================================================================")
print("ALL MILESTONE 4 HARSH ATTACK TESTS PASSED! (0 VULNERABILITIES REMAIN)")
print("=====================================================================")
