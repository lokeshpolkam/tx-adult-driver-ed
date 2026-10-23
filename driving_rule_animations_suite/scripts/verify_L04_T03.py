import os
import json
from playwright.sync_api import sync_playwright

output_dir = 'C:/tx_dmv/driving_rule_animations_suite/verification_frames/L04_T03'
os.makedirs(output_dir, exist_ok=True)

sim_path = 'file:///C:/tx_dmv/driving_rule_animations_suite/simulations/L04_T03_pavement_markings_passing.html'

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
        
        overlap = not (box_a['right'] < box_b['left'] or 
                       box_a['left'] > box_b['right'] or 
                       box_a['bottom'] < box_b['top'] or 
                       box_a['top'] > box_b['bottom'])
        return overlap, { "box_a": box_a, "box_b": box_b }

    print("=== TEST 1: Step 1 Impediment & Sightline Check (t = 0.5s) ===")
    page.click('button[data-step="1"]')
    page.wait_for_timeout(300)
    page.screenshot(path=os.path.join(output_dir, 'step1_broken_yellow_sightline_check.png'))
    overlap_as_tags, _ = check_overlap('#tag-veh-a', '#tag-veh-s')
    overlap_as_veh, _ = check_overlap('#veh-a-container', '#veh-s-container')
    print(f"Step 1 Overlaps: Tags: {overlap_as_tags}, Vehicles: {overlap_as_veh}")

    print("=== TEST 2: Step 2 100-Ft Signal & Pullout (t = 2.5s) ===")
    page.click('button[data-step="2"]')
    page.wait_for_timeout(300)
    page.screenshot(path=os.path.join(output_dir, 'step2_100ft_signal_and_pullout.png'))
    overlap_as_tags, _ = check_overlap('#tag-veh-a', '#tag-veh-s')
    overlap_as_veh, _ = check_overlap('#veh-a-container', '#veh-s-container')
    print(f"Step 2 Overlaps: Tags: {overlap_as_tags}, Vehicles: {overlap_as_veh}")

    print("=== TEST 3: Step 3 Overtaking Traversal in Lane 2 (t = 4.8s) ===")
    page.click('button[data-step="3"]')
    page.wait_for_timeout(300)
    page.screenshot(path=os.path.join(output_dir, 'step3_overtaking_in_passing_lane.png'))
    overlap_as_tags, _ = check_overlap('#tag-veh-a', '#tag-veh-s')
    overlap_as_veh, _ = check_overlap('#veh-a-container', '#veh-s-container')
    
    # Measure lateral/vertical distance between Vehicle A in Lane 2 and Vehicle S in Lane 1
    dist_info = page.evaluate('''() => {
        const a = document.querySelector("#veh-a-container").getBoundingClientRect();
        const s = document.querySelector("#veh-s-container").getBoundingClientRect();
        const ax = a.left + a.width / 2;
        const ay = a.top + a.height / 2;
        const sx = s.left + s.width / 2;
        const sy = s.top + s.height / 2;
        const dx = ax - sx;
        const dy = ay - sy;
        const dist = Math.sqrt(dx * dx + dy * dy);
        return { ax, ay, sx, sy, dx, dy, dist, aBottom: a.bottom, sTop: s.top };
    }''')
    print(f"Step 3 Overlaps: Tags: {overlap_as_tags}, Vehicles: {overlap_as_veh}")
    print(f"Step 3 Center Distance: {dist_info['dist']:.1f}px (Vehicle A: ({dist_info['ax']:.1f}, {dist_info['ay']:.1f}), Vehicle S: ({dist_info['sx']:.1f}, {dist_info['sy']:.1f}))")
    print(f"Step 3 Vertical Gap between bounding boxes: {dist_info['sTop'] - dist_info['aBottom']:.1f}px")

    print("=== TEST 4: Step 4 200-Ft Buffer Return (t = 6.8s) ===")
    page.click('button[data-step="4"]')
    page.wait_for_timeout(300)
    page.screenshot(path=os.path.join(output_dir, 'step4_200ft_safe_buffer_return.png'))
    overlap_as_tags, _ = check_overlap('#tag-veh-a', '#tag-veh-s')
    overlap_as_veh, _ = check_overlap('#veh-a-container', '#veh-s-container')
    print(f"Step 4 Overlaps: Tags: {overlap_as_tags}, Vehicles: {overlap_as_veh}")

    print("=== TEST 5: Mode 2 Double Solid Yellow Line (t = 3.5s) ===")
    page.click('#scenario-btn-solid')
    page.wait_for_timeout(300)
    page.evaluate("pauseSimulation(); currentTime = 3.5; updateSimulation(3.5);")
    page.wait_for_timeout(300)
    page.screenshot(path=os.path.join(output_dir, 'mode2_double_solid_yellow_no_passing.png'))
    overlap_as_tags, _ = check_overlap('#tag-veh-a', '#tag-veh-s')
    overlap_as_veh, _ = check_overlap('#veh-a-container', '#veh-s-container')
    overlap_pill, _ = check_overlap('#tag-veh-s', '#hud-status-pill')
    print(f"Mode 2 Overlaps: Tags: {overlap_as_tags}, Vehicles: {overlap_as_veh}, Pill: {overlap_pill}")

    print("=== TEST 6: Mode 3 Hazard Demo Illegal Pass Collision (t = 3.5s) ===")
    page.click('#scenario-btn-hazard')
    page.wait_for_timeout(300)
    page.evaluate("pauseSimulation(); currentTime = 3.5; updateSimulation(3.5);")
    page.wait_for_timeout(300)
    page.screenshot(path=os.path.join(output_dir, 'mode3_hazard_illegal_pass_headon_conflict.png'))
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
    print("Lesson 9 verification and capture complete!")
