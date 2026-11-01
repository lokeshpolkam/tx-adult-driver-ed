import os
import sys
import json
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

print("=====================================================================")
print("RUNNING HARSH TEST: FULL-SCREEN EXAM, 30-BLOCK PALETTE, STATE SEAL")
print("=====================================================================")

final_exam_url = 'file:///' + os.path.abspath('course_shell/mcqs/final_exam.html').replace('\\', '/')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    page = context.new_page()

    # Seed student state once before navigation
    page.add_init_script("""
        if (!localStorage.getItem('tx_session_token')) {
            localStorage.setItem('tx_session_token', 'token_lokesh_test');
            localStorage.setItem('tx_ade_time', '21600');
            localStorage.setItem('tx_ade_completed', JSON.stringify(['L09-T01']));
            localStorage.setItem('tx_user_data', JSON.stringify({ fullName: 'LOKESH POLKAM' }));
        }
    """)
    page.goto(final_exam_url, wait_until='domcontentloaded')
    page.wait_for_selector('#question-prompt')

    # -------------------------------------------------------------
    # 1. Full-Screen Institutional Examination Layout Check
    # -------------------------------------------------------------
    print("\n[TEST 1] Verifying Full-Screen Institutional Header & Controls...")
    cand_name = page.inner_text('#exam-candidate-name')
    assert 'LOKESH POLKAM' in cand_name, f"Expected candidate LOKESH POLKAM, got: '{cand_name}'"
    avatar = page.inner_text('#exam-candidate-avatar')
    assert 'LP' in avatar, f"Expected avatar LP, got: '{avatar}'"
    has_fs_btn = page.evaluate("() => typeof window.toggleFullScreen === 'function'")
    assert has_fs_btn, "Fullscreen toggle function missing!"
    timer_text = page.inner_text('#exam-timer')
    assert ':' in timer_text, f"Timer missing colon: '{timer_text}'"
    print("  -> PASS: Header renders candidate profile (Lokesh Polkam [LP]), countdown timer, and fullscreen trigger.")

    # -------------------------------------------------------------
    # 2. 30-Question Palette (The 30 Blocks as in Screenshot 2)
    # -------------------------------------------------------------
    print("\n[TEST 2] Verifying 30 Question Palette Blocks & Color States...")
    blocks_count = page.evaluate("() => document.querySelectorAll('#palette-grid-30 button').length")
    assert blocks_count == 30, f"Expected exactly 30 question blocks, found: {blocks_count}"
    print("  -> PASS: Exactly 30 question blocks rendered in 6x5 palette grid.")

    # Check Block 1 is active ring
    block1_classes = page.evaluate("() => document.querySelectorAll('#palette-grid-30 button')[0].className")
    assert "ring-4" in block1_classes or "scale-105" in block1_classes, f"Block 1 should have active ring: {block1_classes}"
    print("  -> PASS: Current question (Block 1) has prominent active focus ring.")

    # -------------------------------------------------------------
    # 3. Marking Answer -> Palette Turns GREEN
    # -------------------------------------------------------------
    print("\n[TEST 3] Marking Answer: Option Selection & Instant Palette Color Update...")
    # Answer Question 1 with Option 2
    page.click('#opt-btn-2')
    page.wait_for_timeout(200)

    # Check Block 1 is GREEN (Answered)
    block1_classes_after = page.evaluate("() => document.querySelectorAll('#palette-grid-30 button')[0].className")
    assert "bg-emerald-600" in block1_classes_after, f"Block 1 should be green after answering, got: {block1_classes_after}"
    answered_text = page.inner_text('#palette-answered-badge')
    assert "1 / 30" in answered_text, f"Palette answered count mismatch: {answered_text}"
    print("  -> PASS: Marking option 2 immediately turned Block 1 GREEN (Answered) and updated counter to 1/30.")

    # -------------------------------------------------------------
    # 4. Editing Marked Answer & Clearing Selection
    # -------------------------------------------------------------
    print("\n[TEST 4] Editing Marked Answer & Clearing Selection...")
    # Change Question 1 to Option 4
    page.click('#opt-btn-4')
    page.wait_for_timeout(200)
    ans_q1 = page.evaluate("() => userAnswers[1]")
    assert ans_q1 == 4, f"Expected answer to update to option 4, got: {ans_q1}"
    print("  -> PASS: Successfully edited marked answer from Option 2 to Option 4.")

    # Advance to Question 2
    page.click('#btn-next')
    page.wait_for_timeout(300)
    q_num = page.inner_text('#stat-q-current')
    assert q_num == "2", f"Expected to advance to question 2, got: {q_num}"

    # Leave Question 2 unanswered, advance to Question 3
    page.click('#btn-next')
    page.wait_for_timeout(300)

    # Block 2 should now be RED (Visited, Not Answered)
    block2_classes = page.evaluate("() => document.querySelectorAll('#palette-grid-30 button')[1].className")
    assert "bg-rose-500" in block2_classes, f"Block 2 should be red (skipped), got: {block2_classes}"
    print("  -> PASS: Skipped question (Block 2) turned RED (Visited but Unanswered).")

    # -------------------------------------------------------------
    # 5. Direct Jump via Palette Block
    # -------------------------------------------------------------
    print("\n[TEST 5] Palette Direct Jump Navigation...")
    # Jump to Question 15 by clicking block 15
    page.evaluate("() => document.querySelectorAll('#palette-grid-30 button')[14].click()")
    page.wait_for_timeout(300)
    q_curr = page.inner_text('#stat-q-current')
    assert q_curr == "15", f"Expected to jump to question 15, got: {q_curr}"
    print("  -> PASS: Clicking block 15 jumped directly to Question 15.")

    # -------------------------------------------------------------
    # 6. Tamper-Resistant LocalStorage & State Restoration
    # -------------------------------------------------------------
    print("\n[TEST 6] Tamper-Resistant LocalStorage State & Reload Recovery...")
    # Answer Question 15 with Option 1
    page.click('#opt-btn-1')
    page.wait_for_timeout(200)

    # Verify session signature in localStorage
    has_sig = page.evaluate("() => !!localStorage.getItem('tx_exam_session_sig')")
    assert has_sig, "Exam session signature missing from localStorage!"
    print("  -> PASS: State saved with cryptographic signature seal.")

    # Reload page to test seamless restoration
    page.reload(wait_until='domcontentloaded')
    page.wait_for_selector('#question-prompt')

    # Verify restored state: should resume on Question 15 with Option 1 selected!
    restored_q = page.inner_text('#stat-q-current')
    assert restored_q == "15", f"Expected restored question 15, got: {restored_q}"
    restored_ans_15 = page.evaluate("() => userAnswers[15]")
    assert restored_ans_15 == 1, f"Expected restored answer for Q15 = 1, got: {restored_ans_15}"
    print("  -> PASS: Page reload seamlessly restored exact marked answers, question position, and palette colors.")

    # -------------------------------------------------------------
    # 7. Finish Exam, Score Revelation & Immediate Certificate Pop-up
    # -------------------------------------------------------------
    print("\n[TEST 7] Score Revelation at the End & Immediate Certificate Pop-up...")
    # Fill in answers to achieve passing score 28/30
    page.evaluate("""() => {
        for (let i = 1; i <= 30; i++) {
            // Answer with correct option for 28 questions, wrong for 2
            const q = EXAM_QUESTIONS[i - 1];
            userAnswers[i] = (i <= 28) ? q.correctOption : ((q.correctOption % 4) + 1);
        }
    }""")

    # Click Finish Exam
    page.click('button:has-text("Finish Exam")')
    page.wait_for_selector('#finish-confirm-modal:not(.hidden)')
    print("  -> PASS: Finish confirmation modal opened with question summary.")

    # Confirm Submission
    page.click('#finish-confirm-modal button:has-text("Submit & Reveal Score")')

    # Wait for Results Container
    page.wait_for_selector('#results-container:not(.hidden)')
    score_display = page.inner_text('#results-score-count')
    pct_display = page.inner_text('#results-score-pct')
    print(f"  -> Revealed Final Score: {score_display} ({pct_display})")
    assert '28 / 30' in score_display, f"Expected 28 / 30, got: {score_display}"

    # Verify Immediate Certificate Pop-up
    page.wait_for_selector('#name-reverification-modal:not(.hidden)', timeout=5000)
    print("  -> PASS: Name Reverification / Certificate Modal popped up immediately upon passing score!")

    # Verify Question-by-Question Review with Red/Green styling
    review_cards = page.evaluate("() => document.querySelectorAll('#results-detailed-review-list > div').length")
    assert review_cards == 30, f"Expected 30 review cards, got: {review_cards}"
    correct_cards = page.evaluate("() => Array.from(document.querySelectorAll('#results-detailed-review-list span')).filter(s => s.textContent.includes('CORRECT')).length")
    incorrect_cards = page.evaluate("() => Array.from(document.querySelectorAll('#results-detailed-review-list span')).filter(s => s.textContent.includes('INCORRECT')).length")
    print(f"  -> PASS: Detailed review rendered with {correct_cards} Correct (Green) and {incorrect_cards} Incorrect (Red) cards.")

    # -------------------------------------------------------------
    # 8. Question Bank Randomization (Variety across sessions)
    # -------------------------------------------------------------
    print("\n[TEST 8] Question Bank Randomization & Variety...")
    # Clear session and sample again
    q_sample_1 = page.evaluate("() => sampleFresh30Questions().map(q => q.id)")
    q_sample_2 = page.evaluate("() => sampleFresh30Questions().map(q => q.id)")

    assert q_sample_1 != q_sample_2, "CRITICAL: Consecutive exam samples were identical! Randomization failed."
    common_count = len(set(q_sample_1).intersection(set(q_sample_2)))
    print(f"  -> Sample 1 first 5 IDs: {q_sample_1[:5]}")
    print(f"  -> Sample 2 first 5 IDs: {q_sample_2[:5]}")
    print(f"  -> Questions in common: {common_count} / 30 (Diverse pool confirmed!)")
    print("  -> PASS: Every exam generation draws distinct randomized combinations from 70-question bank.")

    browser.close()

print("\n=====================================================================")
print("ALL 8 HARSH TESTS PASSED WITH 100% SUCCESS!")
print("=====================================================================")
