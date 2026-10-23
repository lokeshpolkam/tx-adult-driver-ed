import os
import time
from playwright.sync_api import sync_playwright

output_dir = 'C:/tx_dmv/driving_rule_animations_suite/verification_frames/L04_T02'
os.makedirs(output_dir, exist_ok=True)

sim_path = 'file:///C:/tx_dmv/driving_rule_animations_suite/simulations/L04_T02_flashing_yellow_arrow.html'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    page.goto(sim_path)
    page.wait_for_timeout(1000)

    # 1. Step 1: Signal Identification & Approach (t = 0.5s)
    page.click('button[data-step="1"]')
    page.wait_for_timeout(300)
    page.screenshot(path=os.path.join(output_dir, 'step1_fya_signal_identification.png'))
    print('Captured Step 1 (FYA Approach)')

    # 2. Step 2: Oncoming Traffic Yield Hold (t = 2.5s)
    page.click('button[data-step="2"]')
    page.wait_for_timeout(300)
    page.screenshot(path=os.path.join(output_dir, 'step2_fya_oncoming_yield_hold.png'))
    print('Captured Step 2 (Oncoming Yield Hold)')

    # 3. Step 3: Gap Verification & Clearance (t = 4.5s)
    page.click('button[data-step="3"]')
    page.wait_for_timeout(300)
    page.screenshot(path=os.path.join(output_dir, 'step3_fya_gap_clearance.png'))
    print('Captured Step 3 (Gap Clearance)')

    # 4. Step 4: Lawful Permissive Execution (t = 6.8s)
    page.click('button[data-step="4"]')
    page.wait_for_timeout(300)
    page.screenshot(path=os.path.join(output_dir, 'step4_fya_permissive_execution.png'))
    print('Captured Step 4 (Permissive Execution)')

    # 5. Mode 2: Steady Green Arrow (Protected Turn at t = 3.5s)
    page.click('#scenario-btn-green')
    page.wait_for_timeout(300)
    page.evaluate("pauseSimulation(); currentTime = 3.5; updateSimulation(3.5);")
    page.wait_for_timeout(300)
    page.screenshot(path=os.path.join(output_dir, 'mode2_green_arrow_protected_turn.png'))
    print('Captured Mode 2 (Protected Green Arrow)')

    # 6. Mode 3: Hazard Demo: FYA Failure to Yield Collision (t = 3.5s)
    page.click('#scenario-btn-hazard')
    page.wait_for_timeout(300)
    page.evaluate("pauseSimulation(); currentTime = 3.5; updateSimulation(3.5);")
    page.wait_for_timeout(300)
    page.screenshot(path=os.path.join(output_dir, 'mode3_hazard_fya_failure_to_yield.png'))
    print('Captured Mode 3 (Hazard FYA Failure to Yield Collision)')

    browser.close()
    print("All verification frames captured successfully!")
