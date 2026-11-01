import sys
sys.stdout.reconfigure(encoding='utf-8')
import asyncio
from playwright.async_api import async_playwright

async def run_harsh_tests():
    print("=" * 60)
    print("RUNNING HARSH TESTS: MILESTONE 1 (Regulatory & 6-Hour Timer)")
    print("=" * 60)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1280, 'height': 800})
        
        # Test 1: URL parameter bypass attempt (?preview=true)
        print("\n[ATTACK TEST 1] Attempting ?preview=true bypass on Module 9...")
        await page.goto("file:///c:/tx_dmv/course_shell/player.html?preview=true&topic=L09-T02")
        await page.wait_for_timeout(500)
        
        res = await page.evaluate('''() => {
            return {
                mod9Unlocked: isModuleUnlocked(9),
                topic9Unlocked: isTopicUnlocked('L09-T02'),
                elapsedSeconds: elapsedSeconds
            };
        }''')
        print(f"  Result: mod9Unlocked={res['mod9Unlocked']}, topic9Unlocked={res['topic9Unlocked']}")
        assert res['mod9Unlocked'] == False, "FAIL: Module 9 was unlocked via ?preview=true!"
        assert res['topic9Unlocked'] == False, "FAIL: Topic L09-T02 was unlocked via ?preview=true!"
        print("  >>> PASS: ?preview=true bypass successfully rejected! Module 9 is securely locked.")
        
        # Test 2: Timer stop at exactly 6 hours (21,600s)
        print("\n[ATTACK TEST 2] Attempting to force timer past 21,600 seconds...")
        await page.evaluate('''() => {
            // Set time to 21,598 seconds (2s before 6 hours)
            window.setCourseTime(21598);
        }''')
        # Wait 4 seconds for ticks
        await page.wait_for_timeout(4000)
        
        timer_state = await page.evaluate('''() => {
            return {
                elapsedSeconds: elapsedSeconds,
                displayText: document.getElementById('timer-text')?.textContent || '',
                barWidth: document.getElementById('timer-bar')?.style.width || ''
            };
        }''')
        print(f"  Result after 4s: elapsedSeconds={timer_state['elapsedSeconds']}, text='{timer_state['displayText']}', barWidth='{timer_state['barWidth']}'")
        assert timer_state['elapsedSeconds'] == 21600, f"FAIL: Timer did not stop at 21,600s! Got {timer_state['elapsedSeconds']}"
        assert timer_state['barWidth'] == '100%', f"FAIL: Timer bar width is not 100%! Got {timer_state['barWidth']}"
        print("  >>> PASS: Timer strictly capped and stopped at exactly 21,600 seconds (06:00:00).")
        
        # Test 3: Setting time beyond 21,600s clamps to 21,600s
        print("\n[ATTACK TEST 3] Attempting window.setCourseTime(999999)...")
        await page.evaluate('''() => {
            window.setCourseTime(999999);
        }''')
        clamped_state = await page.evaluate('''() => elapsedSeconds''')
        print(f"  Result of setting 999999s: elapsedSeconds={clamped_state}")
        assert clamped_state == 21600, f"FAIL: Timer did not clamp to 21600! Got {clamped_state}"
        print("  >>> PASS: Timer values > 21,600s are strictly clamped to 21,600s.")
        
        await browser.close()
        
    print("\n" + "=" * 60)
    print("ALL HARSH TESTS FOR MILESTONE 1 PASSED WITH ZERO FAILURES!")
    print("=" * 60)

asyncio.run(run_harsh_tests())
