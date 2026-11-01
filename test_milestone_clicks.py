import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:3000/landing.html', wait_until='networkidle')
        
        # Click milestone 2 (Audio preview)
        await page.click('a[aria-label="Audio Narration"]')
        await asyncio.sleep(0.8)
        y = await page.evaluate('window.scrollY')
        print('Scrolled Y after clicking Audio milestone:', y)
        
        # Click milestone 4 (Pricing)
        await page.click('a[aria-label="Certificate & Pricing"]')
        await asyncio.sleep(0.8)
        y_pricing = await page.evaluate('window.scrollY')
        print('Scrolled Y after clicking Pricing milestone:', y_pricing)

        await browser.close()

asyncio.run(run())
