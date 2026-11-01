import sys
import asyncio
from playwright.async_api import async_playwright

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

async def run_harsh_resumption_tests():
    print("=====================================================================")
    print("🚀 RUNNING HARSH-TEST SUITE: COURSE RESUMPTION & PROGRESSION GUARD")
    print("=====================================================================")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        # -------------------------------------------------------------
        # TEST 1: FRESH USER MUST STRICTLY START AT TOPIC 1 LESSON 1 (L01-T01)
        # -------------------------------------------------------------
        print("\n[TEST 1] Fresh User Initialization (Empty LocalStorage)...")
        ctx1 = await browser.new_context()
        page1 = await ctx1.new_page()
        await page1.goto('file:///C:/tx_dmv/course_shell/player.html')
        await page1.wait_for_function("() => typeof window.getActiveTopicId === 'function'")

        t1_active = await page1.evaluate("() => window.getActiveTopicId()")
        print(f"   -> activeTopicId on load: {t1_active}")
        assert t1_active == 'L01-T01', f"FAIL: Expected L01-T01 for fresh visitor, got {t1_active}"

        # Simulate cloud response returning fresh user data
        await page1.evaluate("""() => {
            window.restoreProgressFromCloud({
                completedTopics: [],
                lastActiveTopic: 'L01-T01',
                unlockedTopicId: 'L01-T01',
                enrollmentStatus: 'ACTIVE',
                totalInstructionalSeconds: 0
            });
        }""")
        t1_cloud = await page1.evaluate("() => window.getActiveTopicId()")
        print(f"   -> activeTopicId after cloud sync: {t1_cloud}")
        assert t1_cloud == 'L01-T01', f"FAIL: Fresh user must remain on L01-T01 after cloud sync, got {t1_cloud}"
        print("   ✅ PASS: Fresh visitor opens strictly at L01-T01!")
        await ctx1.close()

        # -------------------------------------------------------------
        # TEST 2: EXISTING STUDENT RESUMES EXACTLY WHERE STOPPED (e.g. L03-T04)
        # -------------------------------------------------------------
        print("\n[TEST 2] Resumption for Student Stopped at L03-T04...")
        ctx2 = await browser.new_context()
        page2 = await ctx2.new_page()
        # Seed local storage simulating previous study session of an enrolled student
        await page2.goto('file:///C:/tx_dmv/course_shell/player.html')
        await page2.wait_for_function("() => typeof window.getActiveTopicId === 'function'")
        await page2.evaluate("""() => {
            localStorage.setItem('tx_user_active', 'true');
            localStorage.setItem('tx_session_token', 'mock_token_123');
            localStorage.setItem('tx_user_data', JSON.stringify({ email: 'student@example.com', enrollmentStatus: 'ACTIVE' }));
            localStorage.setItem('tx_ade_active', 'L03-T04');
            localStorage.setItem('tx_ade_completed', JSON.stringify([
                'L01-T01', 'L01-T02', 'L01-T03',
                'L02-T01', 'L02-T02', 'L02-T03', 'L02-T04', 'L02-T05', 'L02-T06', 'L02-T07',
                'L03-T01', 'L03-T02', 'L03-T03'
            ]));
            if (typeof window.__syncEnrollmentStatus === 'function') {
                window.__syncEnrollmentStatus(true);
            }
        }""")

        # Simulate cloud progress arriving on student's session
        await page2.evaluate("""() => {
            window.restoreProgressFromCloud({
                completedTopics: [
                    'L01-T01', 'L01-T02', 'L01-T03',
                    'L02-T01', 'L02-T02', 'L02-T03', 'L02-T04', 'L02-T05', 'L02-T06', 'L02-T07',
                    'L03-T01', 'L03-T02', 'L03-T03'
                ],
                lastActiveTopic: 'L03-T04',
                unlockedTopicId: 'L03-T04',
                enrollmentStatus: 'ACTIVE',
                totalInstructionalSeconds: 3600
            });
        }""")
        t2_cloud = await page2.evaluate("() => window.getActiveTopicId()")
        print(f"   -> activeTopicId after cloud sync: {t2_cloud}")
        assert t2_cloud == 'L03-T04', f"FAIL: Student should maintain L03-T04 after cloud sync, got {t2_cloud}"
        print("   ✅ PASS: Student resumes exactly where stopped (L03-T04)!")
        await ctx2.close()

        # -------------------------------------------------------------
        # TEST 3: ROGUE DATA ATTACK — PROGRESSION GUARD BLOCKS PVQ (L09-T01)
        # -------------------------------------------------------------
        print("\n[TEST 3] Rogue / Corrupted Data Attack (Unfinished Modules attempting PVQ)...")
        ctx3 = await browser.new_context()
        page3 = await ctx3.new_page()
        await page3.goto('file:///C:/tx_dmv/course_shell/player.html')
        await page3.wait_for_function("() => typeof window.getActiveTopicId === 'function'")
        
        # Cloud sync attempts to push L09-T01 to user who only completed 2 topics
        await page3.evaluate("""() => {
            window.restoreProgressFromCloud({
                completedTopics: ['L01-T01', 'L01-T02'],
                lastActiveTopic: 'L09-T01',
                unlockedTopicId: 'L09-T01',
                enrollmentStatus: 'ACTIVE',
                totalInstructionalSeconds: 500
            });
        }""")
        t3_cloud = await page3.evaluate("() => window.getActiveTopicId()")
        print(f"   -> activeTopicId after rogue cloud attempt: {t3_cloud}")
        assert t3_cloud != 'L09-T01', f"SECURITY BREACH: Cloud sync pushed unfinished user to L09-T01!"
        assert t3_cloud == 'L01-T03', f"Expected L01-T03, got {t3_cloud}"
        print("   ✅ PASS: Progression Guard successfully intercepted & prevented PVQ bypass!")
        await ctx3.close()

        # -------------------------------------------------------------
        # TEST 4: LEGITIMATE COMPLETION ADVANCES TO PVQ (L09-T01)
        # -------------------------------------------------------------
        print("\n[TEST 4] Legitimate Student (Modules 1-8 100% Complete) Advances to PVQ...")
        ctx4 = await browser.new_context()
        page4 = await ctx4.new_page()
        await page4.goto('file:///C:/tx_dmv/course_shell/player.html')
        await page4.wait_for_function("() => typeof window.getActiveTopicId === 'function'")
        # Generate all 74 topics of Modules 1-8
        all_74 = await page4.evaluate("""() => {
            return ALL_TOPICS.filter(t => !['L09-T01', 'L09-T02'].includes(t.id)).map(t => t.id);
        }""")
        assert len(all_74) == 74, f"Expected 74 topics in Modules 1-8, got {len(all_74)}"

        await page4.evaluate(f"""() => {{
            window.restoreProgressFromCloud({{
                completedTopics: {all_74},
                lastActiveTopic: 'L09-T01',
                unlockedTopicId: 'L09-T01',
                enrollmentStatus: 'ACTIVE',
                totalInstructionalSeconds: 21600
            }});
        }}""")

        t4_active = await page4.evaluate("() => window.getActiveTopicId()")
        print(f"   -> activeTopicId for 74/74 completed student: {t4_active}")
        assert t4_active == 'L09-T01', f"Expected legitimate student to be granted access to L09-T01, got {t4_active}"
        print("   ✅ PASS: Legitimate student completing Modules 1-8 accurately reaches PVQ Checkpoint!")
        await ctx4.close()

        # -------------------------------------------------------------
        # TEST 5: HOME DASHBOARD REFLECTS ACCURATE TOPIC
        # -------------------------------------------------------------
        print("\n[TEST 5] Home Dashboard UI Consistency...")
        ctx5 = await browser.new_context()
        page5 = await ctx5.new_page()
        # Seed student on L02-T05
        await page5.goto('file:///C:/tx_dmv/course_shell/home.html')
        await page5.evaluate("""() => {
            localStorage.setItem('tx_user_active', 'true');
            localStorage.setItem('tx_ade_active', 'L02-T05');
            localStorage.setItem('tx_ade_completed', JSON.stringify(['L01-T01', 'L01-T02', 'L01-T03', 'L02-T01', 'L02-T02', 'L02-T03', 'L02-T04']));
            updateDashboardUI();
        }""")
        active_badge = await page5.text_content('#active-topic-id')
        print(f"   -> Home dashboard active topic badge: {active_badge.strip()}")
        assert active_badge.strip() == 'L02-T05', f"Expected L02-T05 on home dashboard, got {active_badge}"

        # Test fresh user on home dashboard
        await page5.evaluate("""() => {
            localStorage.removeItem('tx_ade_active');
            localStorage.setItem('tx_ade_completed', JSON.stringify([]));
            updateDashboardUI();
        }""")
        fresh_badge = await page5.text_content('#active-topic-id')
        print(f"   -> Fresh user on home dashboard: {fresh_badge.strip()}")
        assert fresh_badge.strip() == 'L01-T01', f"Expected L01-T01 on fresh dashboard, got {fresh_badge}"
        print("   ✅ PASS: Home dashboard reflects accurate active topics!")
        await ctx5.close()

        await browser.close()

    print("\n=====================================================================")
    print("🎉 ALL HARSH RESUMPTION & PROGRESSION GUARD TESTS PASSED (5/5)!")
    print("=====================================================================")

if __name__ == '__main__':
    asyncio.run(run_harsh_resumption_tests())
