import asyncio
import os
import sys

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from playwright.async_api import async_playwright

async def run_harsh_checkout_test():
    print("========================================================================")
    print(" HARSH AUTOMATED TEST: CHECKOUT ZERO-UPSELL VERIFICATION")
    print("========================================================================")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1280, 'height': 900})

        checkout_path = os.path.abspath('course_shell/checkout.html').replace('\\', '/')
        file_url = f"file:///{checkout_path}"
        print(f"Navigating to {file_url}")
        await page.goto(file_url, wait_until='load')
        await page.wait_for_timeout(800)

        # 1. Check removal of rush elements
        rush_box = await page.query_selector('#rush-cert-checkbox')
        rush_row = await page.query_selector('#summary-rush-row')
        assert rush_box is None, "FAIL: #rush-cert-checkbox still exists in checkout.html!"
        assert rush_row is None, "FAIL: #summary-rush-row still exists in checkout.html!"
        print(" -> PASS: #rush-cert-checkbox and #summary-rush-row are completely gone from DOM.")

        # 2. Check page content for upsell text
        body_text = await page.inner_text('body')
        assert "Same-Day Priority Certificate Delivery" not in body_text, "FAIL: 'Same-Day Priority Certificate Delivery' text still present!"
        assert "+$1.00" not in body_text, "FAIL: '+$1.00' upsell amount still present!"
        assert "Priority Certificate Expediting" not in body_text, "FAIL: 'Priority Certificate Expediting' text still present!"
        print(" -> PASS: Zero mentions of rush certificate delivery or upsell fees on checkout.")

        # 3. Check Order Summary & Base Price
        total_price_text = await page.inner_text('#summary-total-price')
        assert "$38.00" in total_price_text, f"FAIL: Expected $38.00 base total, got: {total_price_text}"
        print(f" -> PASS: Total due today is clean $38.00 flat with zero upsells ({total_price_text}).")

        # Capture Desktop Screenshot
        shot_path = "C:/Users/lokes/.gemini/antigravity/brain/53b6ff8a-31ad-46c0-81ee-2b68cf0c4302/clean_checkout_zero_upsells.png"
        await page.screenshot(path=shot_path)
        print(f" -> Saved clean checkout screenshot: {shot_path}")

        # 4. Mobile Viewport (390px iPhone)
        mobile_page = await browser.new_page(viewport={'width': 390, 'height': 844})
        await mobile_page.goto(file_url, wait_until='load')
        await mobile_page.wait_for_timeout(800)

        m_body_text = await mobile_page.inner_text('body')
        assert "Same-Day Priority" not in m_body_text, "FAIL: Mobile still has Same-Day Priority"
        m_total = await mobile_page.inner_text('#summary-total-price')
        assert "$38.00" in m_total, f"FAIL: Expected $38.00 on mobile, got: {m_total}"
        print(" -> PASS: Mobile checkout renders clean zero-upsell view.")

        mobile_shot = "C:/Users/lokes/.gemini/antigravity/brain/53b6ff8a-31ad-46c0-81ee-2b68cf0c4302/clean_checkout_mobile.png"
        await mobile_page.screenshot(path=mobile_shot)
        print(f" -> Saved clean mobile checkout screenshot: {mobile_shot}")

        await browser.close()

    print("\n========================================================================")
    print(" ALL CHECKOUT ZERO-UPSELL HARSH TESTS PASSED WITH 100% SUCCESS!")
    print("========================================================================")

if __name__ == '__main__':
    asyncio.run(run_harsh_checkout_test())
