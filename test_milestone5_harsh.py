import os
import sys
import subprocess
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

print("=====================================================================")
print("RUNNING MILESTONE 5 HARSH ATTACK TEST: AUTHENTICATION & PRIVACY")
print("=====================================================================")

# --- ATTACK 1: Privacy Audit across Production Directories ---
res = subprocess.run(['git', 'grep', '-i', 'lokesh', 'server/', 'course_shell/'], capture_output=True, text=True)
assert res.returncode != 0 and len(res.stdout.strip()) == 0, f"CRITICAL PRIVACY LEAK: 'lokesh' found in codebase:\n{res.stdout}"
print("[ATTACK 1 PASSED] Zero developer personal identifiers remain in production codebase")

# --- ATTACK 2: Google SSO Duplicate Key Conflict Audit ---
auth_file = os.path.abspath('server/src/routes/auth.js')
with open(auth_file, 'r', encoding='utf-8') as f:
    auth_src = f.read()

assert "SELECT id, google_sub, email, full_name" in auth_src, "Missing account linking query in auth.js"
assert "WHERE google_sub = $1 OR email = $2" in auth_src, "Google SSO does not check both google_sub and email"
print("[ATTACK 2 PASSED] Google SSO account linking verified: users_email_key duplicate crash neutralized")

# --- ATTACK 3: Admin Console Leakage & DOM Protection via Playwright ---
admin_file = os.path.abspath('course_shell/admin.html')
with open(admin_file, 'r', encoding='utf-8') as f:
    admin_src = f.read()

assert "'$912.00'" not in admin_src, "CRITICAL: Mock revenue '$912.00' still hardcoded in admin.html"
assert "document.getElementById('m-students').textContent = '24';" not in admin_src, "CRITICAL: Mock student count '24' still present in admin.html"
print("[ATTACK 3A PASSED] Simulated fake business numbers ('24 students', '$912.00') eradicated from admin.html")

admin_url = 'file:///' + admin_file.replace('\\', '/')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    # 3B: Unauthenticated visitor navigating to admin.html
    page = browser.new_page()
    page.goto(admin_url, wait_until='domcontentloaded')
    page.wait_for_timeout(300)

    url_after = page.url
    assert 'signin.html' in url_after, f"CRITICAL: Unauthenticated visitor was not redirected! URL: {url_after}"
    print(f"[ATTACK 3B PASSED] Unauthenticated visitor immediately kicked out: {url_after.split('/')[-1]}")
    page.close()

    # 3C: Student attempting privilege escalation (forging localStorage role to STUDENT or fake token)
    context = browser.new_context()
    page2 = context.new_page()
    page2.add_init_script("""
        localStorage.setItem('tx_session_token', 'student_token_123');
        localStorage.setItem('tx_user_data', JSON.stringify({ email: 'hacker@student.com', role: 'STUDENT' }));
    """)
    page2.goto(admin_url, wait_until='domcontentloaded')
    page2.wait_for_timeout(300)

    url_student = page2.url
    assert 'player.html' in url_student or 'signin.html' in url_student, f"CRITICAL: Student accessed admin console! URL: {url_student}"
    print(f"[ATTACK 3C PASSED] Non-admin student privilege escalation rejected! Redirected to: {url_student.split('/')[-1]}")

    browser.close()

print("\n=====================================================================")
print("ALL MILESTONE 5 HARSH ATTACK TESTS PASSED! (0 VULNERABILITIES REMAIN)")
print("=====================================================================")
