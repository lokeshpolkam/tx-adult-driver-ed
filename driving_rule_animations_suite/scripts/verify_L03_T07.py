import os
import time
from playwright.sync_api import sync_playwright

output_dir = 'C:/tx_dmv/driving_rule_animations_suite/verification_frames/L03_T07'
os.makedirs(output_dir, exist_ok=True)

sim_path = 'file:///C:/tx_dmv/driving_rule_animations_suite/simulations/L03_T07_defensive_quadrant_scanning.html'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    page.goto(sim_path)
    page.wait_for_timeout(1000)

    # 1. Step 1: Fresh Green & Defensive Hold (t = 0.5s)
    page.click('button[data-step="1"]')
    page.wait_for_timeout(300)
    page.screenshot(path=os.path.join(output_dir, 'step1_fresh_green_hold.png'))
    print('Captured Step 1')

    # 2. Step 2: 4-Quadrant Visual Sweep (t = 2.5s)
    page.click('button[data-step="2"]')
    page.wait_for_timeout(300)
    page.screenshot(path=os.path.join(output_dir, 'step2_quadrant_visual_sweep.png'))
    print('Captured Step 2')

    # Also capture Quadrant 3 Threat Detection at t = 3.8s
    page.evaluate("pauseSimulation(); currentTime = 3.8; updateSimulation(3.8);")
    page.wait_for_timeout(300)
    page.screenshot(path=os.path.join(output_dir, 'step2_quadrant3_threat_detected.png'))
    print('Captured Step 2 (Quadrant 3 Threat)')

    # 3. Step 3: Red-Light Runner Hazard Evasion (t = 4.2s)
    page.click('button[data-step="3"]')
    page.wait_for_timeout(300)
    page.screenshot(path=os.path.join(output_dir, 'step3_threat_red_light_runner.png'))
    print('Captured Step 3')

    # 4. Step 4: Clearance & Lawful Entry (t = 6.5s)
    page.click('button[data-step="4"]')
    page.wait_for_timeout(300)
    page.screenshot(path=os.path.join(output_dir, 'step4_lawful_resumption.png'))
    print('Captured Step 4')

    # 5. Hazard Demo: Blind Green Launch (Collision at t = 4.2s)
    page.click('#scenario-btn-hazard')
    page.wait_for_timeout(300)
    page.evaluate("pauseSimulation(); currentTime = 4.2; updateSimulation(4.2);")
    page.wait_for_timeout(300)
    page.screenshot(path=os.path.join(output_dir, 'step3_hazard_blind_green_collision.png'))
    print('Captured Hazard Demo')

    browser.close()
    print("All verification frames captured successfully!")
