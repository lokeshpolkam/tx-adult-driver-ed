import os
import json
from playwright.sync_api import sync_playwright

output_dir = 'C:/tx_dmv/driving_rule_animations_suite/verification_frames/L08_T09'
os.makedirs(output_dir, exist_ok=True)

sim_path = 'file:///C:/tx_dmv/driving_rule_animations_suite/simulations/L08_T09_steer_it_clear_it.html'

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

    print("=== TEST 1: Step 1 Minor Collision & Triage (t = 0.5s) ===")
    page.click('button[data-step="1"]')
    page.wait_for_timeout(400)
    page.screenshot(path=os.path.join(output_dir, 'step1_minor_collision_and_triage.png'))
    overlap_ab_tags, _ = check_overlap('#tag-veh-a', '#tag-veh-b')
    overlap_ac_tags, _ = check_overlap('#tag-veh-a', '#tag-veh-c')
    print(f"Step 1 Overlaps: Tags A-B: {overlap_ab_tags}, Tags A-C: {overlap_ac_tags}")

    print("=== TEST 2: Step 2 4-Way Hazards & Shoulder Egress (t = 2.5s) ===")
    page.click('button[data-step="2"]')
    page.wait_for_timeout(400)
    page.screenshot(path=os.path.join(output_dir, 'step2_hazards_and_shoulder_egress.png'))
    overlap_ab_tags, _ = check_overlap('#tag-veh-a', '#tag-veh-b')
    overlap_ab_veh, _ = check_overlap('#veh-a-container', '#veh-b-container')
    print(f"Step 2 Overlaps: Tags: {overlap_ab_tags}, Vehicles: {overlap_ab_veh}")

    print("=== TEST 3: Step 3 Mainlane Highway Clearance (t = 4.8s) ===")
    page.click('button[data-step="3"]')
    page.wait_for_timeout(400)
    page.screenshot(path=os.path.join(output_dir, 'step3_mainlanes_cleared_to_shoulder.png'))
    overlap_ab_tags, _ = check_overlap('#tag-veh-a', '#tag-veh-b')
    overlap_ab_veh, _ = check_overlap('#veh-a-container', '#veh-b-container')
    
    # Measure clearance distance from Lane 2 to shoulder
    veh_pos = page.evaluate('''() => {
        const a = document.querySelector("#veh-a-container").getBoundingClientRect();
        const b = document.querySelector("#veh-b-container").getBoundingClientRect();
        return { aLeft: a.left, aTop: a.top, bLeft: b.left, bTop: b.top, gapX: a.left - b.right };
    }''')
    print(f"Step 3 Overlaps: Tags: {overlap_ab_tags}, Vehicles: {overlap_ab_veh}")
    print(f"Step 3 Vehicle Coordinates: Veh A: ({veh_pos['aLeft']:.1f}, {veh_pos['aTop']:.1f}), Veh B: ({veh_pos['bLeft']:.1f}, {veh_pos['bTop']:.1f}), Gap: {veh_pos['gapX']:.1f}px")

    print("=== TEST 4: Step 4 Driver Exchange & CR-3 Protocol (t = 6.8s) ===")
    page.click('button[data-step="4"]')
    page.wait_for_timeout(400)
    page.screenshot(path=os.path.join(output_dir, 'step4_driver_exchange_and_cr3.png'))
    overlap_ab_tags, _ = check_overlap('#tag-veh-a', '#tag-veh-b')
    overlap_bp_tags, _ = check_overlap('#tag-veh-b', '#tag-veh-police')
    overlap_bp_veh, _ = check_overlap('#veh-b-container', '#veh-police-container')
    print(f"Step 4 Overlaps: Tags A-B: {overlap_ab_tags}, Tags B-Police: {overlap_bp_tags}, Vehicles B-Police: {overlap_bp_veh}")

    print("=== TEST 5: Mode 2 Unlawful Lane Blockage (t = 3.5s) ===")
    page.click('#scenario-btn-blocked')
    page.wait_for_timeout(300)
    page.evaluate('pauseSimulation(); currentTime = 3.5; updateSimulation(3.5);')
    page.wait_for_timeout(300)
    page.screenshot(path=os.path.join(output_dir, 'mode2_unlawful_lane_blockage.png'))
    overlap_ab_tags, _ = check_overlap('#tag-veh-a', '#tag-veh-b')
    overlap_ac_tags, _ = check_overlap('#tag-veh-a', '#tag-veh-c')
    overlap_bc_tags, _ = check_overlap('#tag-veh-b', '#tag-veh-c')
    print(f"Mode 2 Overlaps: Tags A-B: {overlap_ab_tags}, Tags A-C: {overlap_ac_tags}, Tags B-C: {overlap_bc_tags}")

    print("=== TEST 6: Mode 3 Hazard Demo Secondary Collision (t = 3.5s) ===")
    page.click('#scenario-btn-hazard')
    page.wait_for_timeout(300)
    page.evaluate('pauseSimulation(); currentTime = 3.5; updateSimulation(3.5);')
    page.wait_for_timeout(300)
    page.screenshot(path=os.path.join(output_dir, 'mode3_secondary_impact_hazard.png'))
    overlap_pill, _ = check_overlap('#stage-status-pill', '#tag-veh-a')
    overlap_ac_tags, _ = check_overlap('#tag-veh-a', '#tag-veh-c')
    print(f"Mode 3 Overlap: Pill/Veh A: {overlap_pill}, Tags A-C: {overlap_ac_tags}")

    print("\n=== CONSOLE LOGS & ERRORS ===")
    print(f"Total Console Logs: {len(console_logs)}")
    for log in console_logs:
        if 'error' in log.lower() or 'warning' in log.lower():
            print(f"   {log}")
    print(f"Total JS Errors: {len(js_errors)}")
    for err in js_errors:
        print(f"   [JS ERROR] {err}")

    assert len(js_errors) == 0, f"Encountered {len(js_errors)} JavaScript errors!"
    print("Lesson 33 (L08-T09) verification and capture complete!")

    browser.close()
