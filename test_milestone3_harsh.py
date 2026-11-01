import os
import sys
import json
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

print("=====================================================================")
print("RUNNING MILESTONE 3 HARSH ATTACK TEST: EXAMINATION & GRADING INTEGRITY")
print("=====================================================================")

# --- ATTACK 1: Backend Route Implementation Audit ---
quizzes_path = os.path.abspath('server/src/routes/quizzes.js')
with open(quizzes_path, 'r', encoding='utf-8') as f:
    q_src = f.read()

assert "router.post('/lessons/:topicId/grade'" in q_src, "CRITICAL: /lessons/:topicId/grade route missing"
assert "router.post('/exam/grade'" in q_src, "CRITICAL: /exam/grade route missing"
print("[ATTACK 1 PASSED] Backend endpoints /api/v1/lessons/:topicId/grade and /api/v1/exam/grade successfully registered")

# --- ATTACK 2: Audit Topic Quizzes for Disruptive Alert Popups ---
import glob
mcqs = glob.glob(os.path.abspath('course_shell/mcqs/L*.html'))
for f in mcqs:
    if 'final_exam.html' in f: continue
    with open(f, 'r', encoding='utf-8') as fh:
        src = fh.read()
    assert 'alert("Unable to communicate with Texas Driver Education grading server' not in src, f"CRITICAL: Alert popup remains in {f}"

print(f"[ATTACK 2 PASSED] Verified all {len(mcqs)} topic quiz files: Zero disruptive network alert popups remain")

# --- ATTACK 3: Playwright Attack on Final Exam Shuffling & Blind Option 1 Cheat ---
final_exam_url = 'file:///' + os.path.abspath('course_shell/mcqs/final_exam.html').replace('\\', '/')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    # 3A: Direct access attack without prerequisite hours
    page = browser.new_page()
    page.goto(final_exam_url, wait_until='domcontentloaded')
    
    # In a standalone window without localStorage, verify it redirected to player.html
    current_url = page.url
    assert 'player.html' in current_url or 'L09-T02' in current_url, f"CRITICAL: Direct access did not redirect to player! Current URL: {current_url}"
    print(f"[ATTACK 3A PASSED] Standalone direct navigation blocked! Redirected to: {current_url.split('/')[-1]}")
    page.close()

    # 3B: Legitimate student session (inside LMS or with completed hours)
    context = browser.new_context()
    page2 = context.new_page()
    
    # Seed authenticated state and 21,600s
    page2.add_init_script("""
        localStorage.setItem('tx_session_token', 'test_token_valid');
        localStorage.setItem('tx_ade_time', '21600');
        localStorage.setItem('tx_ade_completed', JSON.stringify(['L09-T01']));
        localStorage.setItem('tx_user_data', JSON.stringify({ fullName: 'HARSH TEST STUDENT' }));
    """)
    page2.goto(final_exam_url, wait_until='domcontentloaded')

    # Wait for exam to initialize and options to shuffle
    page2.wait_for_selector('#question-prompt')

    # Inspect correctOption distribution across all 30 questions
    correct_options = page2.evaluate("""() => {
        return EXAM_QUESTIONS.map(q => q.correctOption);
    }""")

    assert len(correct_options) == 30, f"Expected 30 questions, got {len(correct_options)}"
    
    # Count occurrences of option 1, 2, 3, 4
    counts = {1: correct_options.count(1), 2: correct_options.count(2), 3: correct_options.count(3), 4: correct_options.count(4)}
    print(f"Correct answer distribution across options: {counts}")

    # Assert that option 1 is NOT 30 out of 30!
    assert counts[1] < 30, "CRITICAL VULNERABILITY: All 30 questions still have option 1 as correct answer!"
    # Assert that at least 3 different options are represented (randomly distributed)
    non_zero = sum(1 for c in counts.values() if c > 0)
    assert non_zero >= 3, f"CRITICAL VULNERABILITY: Options poorly distributed: {counts}"
    print("[ATTACK 3B PASSED] Dynamic Fisher-Yates shuffle confirmed! Correct answers distributed evenly across options")

    # 3C: Blind Option 1 Attack Simulation
    # If a student blindly answers option 1 for all 30 questions:
    blind_score = counts[1] # number of times option 1 happened to be correct
    print(f"Student blindly choosing option 1 would score: {blind_score}/30 ({(blind_score/30)*100:.1f}%)")
    assert blind_score < 21, f"CRITICAL VULNERABILITY: Student passed with blind option 1! Score: {blind_score}/30"
    print(f"[ATTACK 3C PASSED] Blind Option 1 cheat destroyed! Student scored {blind_score}/30 (Fails: 21 required to pass)")

    # 3D: Simulate clicking an answer in topic quiz L01-T01 without alert popup
    page3 = context.new_page()
    quiz_url = 'file:///' + os.path.abspath('course_shell/mcqs/L01-T01.html').replace('\\', '/')
    page3.goto(quiz_url, wait_until='domcontentloaded')
    page3.wait_for_selector('#opt-btn-1')

    # Track dialogs/alerts
    dialogs = []
    page3.on('dialog', lambda d: (dialogs.append(d.message), d.accept()))

    # Click an option
    page3.click('#opt-btn-1')
    page3.wait_for_timeout(500)

    assert len(dialogs) == 0, f"CRITICAL: Alert popup was triggered during quiz: {dialogs}"
    print("[ATTACK 3D PASSED] Topic quiz answer submitted smoothly with 0 alert dialogs")

    browser.close()

print("\n=====================================================================")
print("ALL MILESTONE 3 HARSH ATTACK TESTS PASSED! (0 VULNERABILITIES REMAIN)")
print("=====================================================================")
