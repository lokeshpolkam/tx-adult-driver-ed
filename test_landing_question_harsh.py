import asyncio
import os
import sys

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from playwright.async_api import async_playwright

async def run_harsh_landing_test():
    print("========================================================================")
    print(" HARSH AUTOMATED TEST: LANDING PAGE SAMPLE EXAM QUESTION RESTRUCTURING")
    print("========================================================================")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # Test 1: Desktop Viewport & DOM Structure
        print("\n[TEST 1] Testing Desktop Placement & DOM Order...")
        page = await browser.new_page(viewport={'width': 1280, 'height': 900})
        
        # We can serve via local file path or http-server
        landing_path = os.path.abspath('course_shell/landing.html').replace('\\', '/')
        file_url = f"file:///{landing_path}"
        await page.goto(file_url, wait_until='load')
        await page.wait_for_timeout(800)

        # Check section existence
        hero = await page.query_selector('#hero')
        how_it_works = await page.query_selector('#how-it-works')
        sample_q = await page.query_selector('#sample-exam-question')
        audio_prev = await page.query_selector('#audio-preview')
        curriculum = await page.query_selector('#curriculum')

        assert hero is not None, "FAIL: #hero not found"
        assert how_it_works is not None, "FAIL: #how-it-works not found"
        assert sample_q is not None, "FAIL: #sample-exam-question not found"
        assert audio_prev is not None, "FAIL: #audio-preview not found"
        assert curriculum is not None, "FAIL: #curriculum not found"
        print(" -> All core sections exist.")

        # Test DOM order: hero < how_it_works < sample_q < audio_prev
        dom_order = await page.evaluate('''() => {
            const h = document.getElementById('hero');
            const hiw = document.getElementById('how-it-works');
            const sq = document.getElementById('sample-exam-question');
            const ap = document.getElementById('audio-preview');
            
            // compareDocumentPosition: 4 means Node B follows Node A
            const h_before_hiw = (h.compareDocumentPosition(hiw) & 4) !== 0;
            const hiw_before_sq = (hiw.compareDocumentPosition(sq) & 4) !== 0;
            const sq_before_ap = (sq.compareDocumentPosition(ap) & 4) !== 0;
            
            return { h_before_hiw, hiw_before_sq, sq_before_ap };
        }''')

        assert dom_order['h_before_hiw'], "FAIL: #hero must be before #how-it-works"
        assert dom_order['hiw_before_sq'], "FAIL: #how-it-works must be before #sample-exam-question"
        assert dom_order['sq_before_ap'], "FAIL: #sample-exam-question must be pushed up before #audio-preview"
        print(" -> PASS: #sample-exam-question is successfully pushed up right after #how-it-works and before #audio-preview!")

        # Test 2: Complete removal of Question 2
        print("\n[TEST 2] Verifying Complete Removal of Question 2 & Switcher Tabs...")
        q2_tab = await page.query_selector('#tab-btn-moveover')
        q1_tab = await page.query_selector('#tab-btn-25d')
        q2_scenario = await page.query_selector('#exam-scenario-moveover')
        q2_quiz = await page.query_selector('#sample-quiz-moveover')
        q2_feedback = await page.query_selector('#quiz-feedback-moveover')

        assert q2_tab is None, "FAIL: #tab-btn-moveover still exists in DOM"
        assert q1_tab is None, "FAIL: #tab-btn-25d switcher tab should be removed (only single question remains)"
        assert q2_scenario is None, "FAIL: #exam-scenario-moveover still exists in DOM"
        assert q2_quiz is None, "FAIL: #sample-quiz-moveover still exists in DOM"
        assert q2_feedback is None, "FAIL: #quiz-feedback-moveover still exists in DOM"
        print(" -> PASS: Question 2 tabs and scenario DOM nodes are completely removed.")

        # Check badge and headings have no "0 / 2" or "Scenario 1 of 2"
        page_text = await sample_q.inner_text()
        assert "0 / 2" not in page_text, f"FAIL: Still mentions '0 / 2': {page_text}"
        assert "1 of 2" not in page_text, f"FAIL: Still mentions '1 of 2': {page_text}"
        assert "TTC § 545.151" in page_text, "FAIL: Statutory citation TTC § 545.151 missing"
        print(" -> PASS: Text correctly reflects single official question without dual-scenario counters.")

        # Test 3: Interactive 2.5D Diorama Simulation & Step Controls
        print("\n[TEST 3] Testing 2.5D Diorama Interactivity & Simulation Controls...")
        await sample_q.scroll_into_view_if_needed()
        await page.wait_for_timeout(500)

        # Check step buttons
        step1 = await page.query_selector('#m-step-1')
        step2 = await page.query_selector('#m-step-2')
        step3 = await page.query_selector('#m-step-3')
        step4 = await page.query_selector('#m-step-4')
        assert all([step1, step2, step3, step4]), "FAIL: Step buttons 1-4 not found"

        # Click step 2
        await step2.click()
        await page.wait_for_timeout(200)
        hud_a_text = await page.inner_text('#m-hud-vehA')
        assert "YIELDING" in hud_a_text or "MPH" in hud_a_text, f"Unexpected HUD text on Step 2: {hud_a_text}"
        print(f" -> Step 2 Telemetry HUD: {hud_a_text}")

        # Test 4: Answering Incorrectly (Option B)
        print("\n[TEST 4] Testing Incorrect Choice (Option B)...")
        opt_b = await page.query_selector('#quiz-opt-2')
        assert opt_b is not None, "FAIL: Option B not found"
        await opt_b.click()
        await page.wait_for_timeout(300)

        fb_el = await page.query_selector('#quiz-feedback')
        assert fb_el is not None and await fb_el.is_visible(), "FAIL: Feedback container not visible on wrong answer"
        fb_text = await fb_el.inner_text()
        assert "INCORRECT" in fb_text, f"FAIL: Wrong feedback text: {fb_text}"
        assert "TTC § 545.151" in fb_text, "FAIL: Statutory citation missing from wrong feedback"
        print(" -> PASS: Option B correctly displays statutory correction feedback.")

        # Test 5: Answering Correctly (Option A)
        print("\n[TEST 5] Testing Correct Choice (Option A)...")
        opt_a = await page.query_selector('#quiz-opt-1')
        assert opt_a is not None, "FAIL: Option A not found"
        await opt_a.click()
        await page.wait_for_timeout(500)

        fb_text_correct = await fb_el.inner_text()
        assert "100% CORRECT" in fb_text_correct, f"FAIL: Correct feedback text missing: {fb_text_correct}"
        assert "Enroll Now" in fb_text_correct, "FAIL: CTA button 'Enroll Now' missing in success feedback"
        
        # Check badge updated
        badge_text = await page.inner_text('#exam-score-badge')
        assert "100% PASSED" in badge_text or "EXAM READY" in badge_text, f"FAIL: Score badge not updated: {badge_text}"
        print(f" -> Status badge updated to: {badge_text}")
        print(" -> PASS: Option A correctly triggers celebration, statutory pass, and dynamic enroll CTA.")

        # Capture Desktop Screenshot
        desktop_shot = "C:/Users/lokes/.gemini/antigravity/brain/53b6ff8a-31ad-46c0-81ee-2b68cf0c4302/sample_question_upgraded_desktop.png"
        await sample_q.screenshot(path=desktop_shot)
        print(f" -> Saved desktop screenshot: {desktop_shot}")

        # Test 6: Mobile Responsiveness (390px iPhone Viewport)
        print("\n[TEST 6] Testing Mobile 390px iPhone Responsiveness...")
        mobile_page = await browser.new_page(viewport={'width': 390, 'height': 844})
        await mobile_page.goto(file_url, wait_until='load')
        await mobile_page.wait_for_timeout(800)

        m_sample_q = await mobile_page.query_selector('#sample-exam-question')
        assert m_sample_q is not None, "FAIL: Mobile #sample-exam-question not found"
        await m_sample_q.scroll_into_view_if_needed()
        await mobile_page.wait_for_timeout(500)

        # Check for horizontal scroll overflow
        overflow = await mobile_page.evaluate('''() => {
            return {
                scrollWidth: document.documentElement.scrollWidth,
                innerWidth: window.innerWidth,
                hasOverflow: document.documentElement.scrollWidth > window.innerWidth
            };
        }''')
        assert not overflow['hasOverflow'], f"FAIL: Mobile horizontal overflow detected: {overflow}"
        print(f" -> PASS: Zero mobile overflow on 390px viewport (scrollWidth: {overflow['scrollWidth']}, innerWidth: {overflow['innerWidth']}).")

        # Answer Option A on mobile
        m_opt_a = await mobile_page.query_selector('#quiz-opt-1')
        await m_opt_a.click()
        await mobile_page.wait_for_timeout(500)

        # Capture Mobile Screenshot
        mobile_shot = "C:/Users/lokes/.gemini/antigravity/brain/53b6ff8a-31ad-46c0-81ee-2b68cf0c4302/sample_question_upgraded_mobile.png"
        await m_sample_q.screenshot(path=mobile_shot)
        print(f" -> Saved mobile screenshot: {mobile_shot}")

        # Test 7: Verify index.html is identical and works equally
        print("\n[TEST 7] Verifying course_shell/index.html is identical to landing.html...")
        with open('course_shell/landing.html', 'r', encoding='utf-8') as f1, open('course_shell/index.html', 'r', encoding='utf-8') as f2:
            t1 = f1.read()
            t2 = f2.read()
        assert t1 == t2, "FAIL: course_shell/index.html does not match course_shell/landing.html!"
        print(" -> PASS: index.html and landing.html are 100% in parity.")

        await browser.close()

    print("\n========================================================================")
    print(" ALL 7 HARSH LANDING QUESTION TESTS PASSED WITH 100% SUCCESS!")
    print("========================================================================")

if __name__ == '__main__':
    asyncio.run(run_harsh_landing_test())
