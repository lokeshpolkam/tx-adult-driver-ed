import os
import json
from playwright.sync_api import sync_playwright

sim_path = 'file:///C:/tx_dmv/driving_rule_animations_suite/simulations/L04_T02_flashing_yellow_arrow.html'
output_dir = 'C:/tx_dmv/driving_rule_animations_suite/verification_frames/L04_T02'

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
            return False, "One or both elements invisible"
        
        # Check collision with a 2px buffer
        overlap = not (box_a['right'] < box_b['left'] or 
                       box_a['left'] > box_b['right'] or 
                       box_a['bottom'] < box_b['top'] or 
                       box_a['top'] > box_b['bottom'])
        return overlap, { "box_a": box_a, "box_b": box_b }

    print("=== TEST 1: Initial Render & Step 1 ===")
    page.click('button[data-step="1"]')
    page.wait_for_timeout(300)
    overlap_ab_tags, _ = check_overlap('#tag-veh-a', '#tag-veh-b')
    overlap_ab_veh, _ = check_overlap('#veh-a-container', '#veh-b-container')
    overlap_a_pill, _ = check_overlap('#tag-veh-a', '#hud-signal-pill')
    overlap_b_pill, _ = check_overlap('#tag-veh-b', '#hud-signal-pill')
    print(f"Step 1 Overlaps: Tags: {overlap_ab_tags}, Vehicles: {overlap_ab_veh}, Tag A/Pill: {overlap_a_pill}, Tag B/Pill: {overlap_b_pill}")

    print("=== TEST 2: Step 2 Oncoming Yield Hold (t = 2.5s) ===")
    page.click('button[data-step="2"]')
    page.wait_for_timeout(300)
    overlap_ab_tags, details_tags = check_overlap('#tag-veh-a', '#tag-veh-b')
    overlap_ab_veh, details_veh = check_overlap('#veh-a-container', '#veh-b-container')
    overlap_a_pill, _ = check_overlap('#tag-veh-a', '#hud-signal-pill')
    overlap_b_pill, _ = check_overlap('#tag-veh-b', '#hud-signal-pill')
    
    # Calculate vehicle center distance in Step 2
    dist_info = page.evaluate('''() => {
        const a = document.querySelector("#veh-a-container").getBoundingClientRect();
        const b = document.querySelector("#veh-b-container").getBoundingClientRect();
        const ax = a.left + a.width / 2;
        const ay = a.top + a.height / 2;
        const bx = b.left + b.width / 2;
        const by = b.top + b.height / 2;
        const dx = ax - bx;
        const dy = ay - by;
        const dist = Math.sqrt(dx * dx + dy * dy);
        return { ax, ay, bx, by, dx, dy, dist, aBottom: a.bottom, bTop: b.top, bBottom: b.bottom, aTop: a.top };
    }''')
    print(f"Step 2 Overlaps: Tags: {overlap_ab_tags}, Vehicles: {overlap_ab_veh}")
    print(f"Step 2 Physical Distance: {dist_info['dist']:.1f}px (Vehicle A Center: ({dist_info['ax']:.1f}, {dist_info['ay']:.1f}), Vehicle B Center: ({dist_info['bx']:.1f}, {dist_info['by']:.1f}))")
    print(f"Step 2 Vertical Gap between boxes: {dist_info['aTop'] - dist_info['bBottom']:.1f}px")

    print("=== TEST 3: Step 3 Gap Clearance (t = 4.5s) ===")
    page.click('button[data-step="3"]')
    page.wait_for_timeout(300)
    overlap_ab_tags, _ = check_overlap('#tag-veh-a', '#tag-veh-b')
    overlap_ab_veh, _ = check_overlap('#veh-a-container', '#veh-b-container')
    print(f"Step 3 Overlaps: Tags: {overlap_ab_tags}, Vehicles: {overlap_ab_veh}")

    print("=== TEST 4: Step 4 Permissive Execution (t = 6.8s) ===")
    page.click('button[data-step="4"]')
    page.wait_for_timeout(300)
    overlap_ab_tags, _ = check_overlap('#tag-veh-a', '#tag-veh-b')
    overlap_ab_veh, _ = check_overlap('#veh-a-container', '#veh-b-container')
    print(f"Step 4 Overlaps: Tags: {overlap_ab_tags}, Vehicles: {overlap_ab_veh}")

    print("=== TEST 5: Mode 2 Green Arrow (Protected Turn) ===")
    page.click('#scenario-btn-green')
    page.wait_for_timeout(300)
    page.evaluate("pauseSimulation(); currentTime = 3.5; updateSimulation(3.5);")
    page.wait_for_timeout(300)
    overlap_ab_tags, _ = check_overlap('#tag-veh-a', '#tag-veh-b')
    overlap_ab_veh, _ = check_overlap('#veh-a-container', '#veh-b-container')
    overlap_b_pill, details_b_pill = check_overlap('#tag-veh-b', '#hud-signal-pill')
    print(f"Mode 2 Overlaps: Tags: {overlap_ab_tags}, Vehicles: {overlap_ab_veh}, Tag B/Pill: {overlap_b_pill}")

    print("=== TEST 6: Mode 3 Hazard Demo (FYA Failure to Yield) ===")
    page.click('#scenario-btn-hazard')
    page.wait_for_timeout(300)
    page.evaluate("pauseSimulation(); currentTime = 3.5; updateSimulation(3.5);")
    page.wait_for_timeout(300)
    overlap_banner_hud, _ = check_overlap('#hazard-banner', '#telemetry-hud-card')
    print(f"Mode 3 Overlap: Banner/HUD: {overlap_banner_hud}")

    print("\n=== CONSOLE LOGS & ERRORS ===")
    print(f"Total Console Logs: {len(console_logs)}")
    for l in console_logs:
        print("  ", l)
    print(f"Total JS Errors: {len(js_errors)}")
    for e in js_errors:
        print("  ERROR:", e)

    browser.close()
