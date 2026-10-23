import os
import json
from playwright.sync_api import sync_playwright

output_dir = 'C:/tx_dmv/driving_rule_animations_suite/verification_frames/L04_T04'
os.makedirs(output_dir, exist_ok=True)

sim_path = 'file:///C:/tx_dmv/driving_rule_animations_suite/simulations/L04_T04_dark_malfunctioning_signals.html'

console_logs = []
js_errors = []

def handle_console(msg):
    console_logs.append(f"[{msg.type}] {msg.text}")

def handle_page_error(err):
    js_errors.append(str(err))

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    page.on("console", handle_console)
    page.on("pageerror", handle_page_error)
    
    page.goto(sim_path)
    page.wait_for_timeout(1000)

    # Helper function to check overlap between two elements
    def check_overlap(selector_a, selector_b):
        box_a = page.evaluate(f'''() => {{
            const el = document.querySelector("{selector_a}");
            if (!el || window.getComputedStyle(el).opacity === "0" || window.getComputedStyle(el).display === "none") return null;
            const r = el.getBoundingClientRect();
            return {{ left: r.left, top: r.top, right: r.right, bottom: r.bottom, width: r.width, height: r.height }};
        }}''')
        box_b = page.evaluate(f'''() => {{
            const el = document.querySelector("{selector_b}");
            if (!el || window.getComputedStyle(el).opacity === "0" || window.getComputedStyle(el).display === "none") return null;
            const r = el.getBoundingClientRect();
            return {{ left: r.left, top: r.top, right: r.right, bottom: r.bottom, width: r.width, height: r.height }};
        }}''')
        if not box_a or not box_b:
            return False, None
        
        # Check standard bounding box overlap (with 2px buffer for border/rounding)
        overlap_x = max(0, min(box_a['right'], box_b['right']) - max(box_a['left'], box_b['left']))
        overlap_y = max(0, min(box_a['bottom'], box_b['bottom']) - max(box_a['top'], box_b['top']))
        is_overlapping = (overlap_x > 2 and overlap_y > 2)
        return is_overlapping, (box_a, box_b)

    print("=== TEST 1: Step 1 Dark Signal Perception & Decel (t = 0.5s) ===")
    page.click('button[data-step="1"]')
    page.wait_for_timeout(300)
    page.screenshot(path=os.path.join(output_dir, 'step1_dark_signal_perception_decel.png'))
    overlap_ab_tags, _ = check_overlap('#tag-veh-a', '#tag-veh-b')
    overlap_ab_veh, _ = check_overlap('#veh-a-container', '#veh-b-container')
    print(f"Step 1 Overlaps: Tags: {overlap_ab_tags}, Vehicles: {overlap_ab_veh}")

    print("=== TEST 2: Step 2 Dual Full Halt at Stop Bars (t = 2.5s) ===")
    page.click('button[data-step="2"]')
    page.wait_for_timeout(300)
    page.screenshot(path=os.path.join(output_dir, 'step2_dual_full_halt_at_stop_bars.png'))
    overlap_ab_tags, _ = check_overlap('#tag-veh-a', '#tag-veh-b')
    overlap_ab_veh, _ = check_overlap('#veh-a-container', '#veh-b-container')
    print(f"Step 2 Overlaps: Tags: {overlap_ab_tags}, Vehicles: {overlap_ab_veh}")

    # Measure distance at dual halt
    dist_step2 = page.evaluate('''() => {
        const a = document.querySelector("#veh-a-container").getBoundingClientRect();
        const b = document.querySelector("#veh-b-container").getBoundingClientRect();
        const ax = a.left + a.width/2, ay = a.top + a.height/2;
        const bx = b.left + b.width/2, by = b.top + b.height/2;
        const dist = Math.sqrt((ax-bx)**2 + (ay-by)**2);
        return { dist, ax, ay, bx, by };
    }''')
    print(f"Step 2 Center Distance: {dist_step2['dist']:.1f}px (A: ({dist_step2['ax']:.1f}, {dist_step2['ay']:.1f}), B: ({dist_step2['bx']:.1f}, {dist_step2['by']:.1f}))")

    print("=== TEST 3: Step 3 Vehicle A Precedence Traversal (t = 4.8s) ===")
    page.click('button[data-step="3"]')
    page.wait_for_timeout(300)
    page.screenshot(path=os.path.join(output_dir, 'step3_vehicle_a_precedence_traversal.png'))
    overlap_ab_tags, _ = check_overlap('#tag-veh-a', '#tag-veh-b')
    overlap_ab_veh, _ = check_overlap('#veh-a-container', '#veh-b-container')
    print(f"Step 3 Overlaps: Tags: {overlap_ab_tags}, Vehicles: {overlap_ab_veh}")

    dist_step3 = page.evaluate('''() => {
        const a = document.querySelector("#veh-a-container").getBoundingClientRect();
        const b = document.querySelector("#veh-b-container").getBoundingClientRect();
        const ax = a.left + a.width/2, ay = a.top + a.height/2;
        const bx = b.left + b.width/2, by = b.top + b.height/2;
        const dist = Math.sqrt((ax-bx)**2 + (ay-by)**2);
        return { dist, ax, ay, bx, by };
    }''')
    print(f"Step 3 Center Distance: {dist_step3['dist']:.1f}px (A: ({dist_step3['ax']:.1f}, {dist_step3['ay']:.1f}), B: ({dist_step3['bx']:.1f}, {dist_step3['by']:.1f}))")

    print("=== TEST 4: Step 4 Clearance & Secondary Traversal (t = 6.8s) ===")
    page.click('button[data-step="4"]')
    page.wait_for_timeout(300)
    page.screenshot(path=os.path.join(output_dir, 'step4_clearance_and_secondary_traversal.png'))
    overlap_ab_tags, _ = check_overlap('#tag-veh-a', '#tag-veh-b')
    overlap_ab_veh, _ = check_overlap('#veh-a-container', '#veh-b-container')
    print(f"Step 4 Overlaps: Tags: {overlap_ab_tags}, Vehicles: {overlap_ab_veh}")

    print("=== TEST 5: Mode 2 Simultaneous Arrival (t = 3.5s) ===")
    page.click('#mode-simult-btn')
    page.wait_for_timeout(300)
    page.evaluate("currentTime = 3.5; updateSimulation(3.5);")
    page.wait_for_timeout(300)
    page.screenshot(path=os.path.join(output_dir, 'mode2_simultaneous_arrival_yield_to_right.png'))
    overlap_m2_tags, _ = check_overlap('#tag-veh-a', '#tag-veh-b')
    overlap_m2_veh, _ = check_overlap('#veh-a-container', '#veh-b-container')
    overlap_m2_pill, _ = check_overlap('#hud-status-pill', '#telemetry-hud-card')
    print(f"Mode 2 Overlaps: Tags: {overlap_m2_tags}, Vehicles: {overlap_m2_veh}, Pill: {overlap_m2_pill}")

    print("=== TEST 6: Mode 3 Hazard Demo Failure to Stop Collision (t = 3.5s) ===")
    page.click('#mode-hazard-btn')
    page.wait_for_timeout(300)
    page.evaluate("currentTime = 3.5; updateSimulation(3.5);")
    page.wait_for_timeout(300)
    page.screenshot(path=os.path.join(output_dir, 'mode3_hazard_failure_to_stop_tbone_collision.png'))
    overlap_banner_hud, _ = check_overlap('#hazard-banner', '#telemetry-hud-card')
    print(f"Mode 3 Overlap: Banner/HUD: {overlap_banner_hud}")

    print("\n=== CONSOLE LOGS & ERRORS ===")
    print(f"Total Console Logs: {len(console_logs)}")
    for log in console_logs:
        print(f"   {log}")
    print(f"Total JS Errors: {len(js_errors)}")
    for err in js_errors:
        print(f"   [ERROR] {err}")

    browser.close()

print("Lesson 10 verification and capture complete!")
