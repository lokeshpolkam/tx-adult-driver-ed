import os
import json
from playwright.sync_api import sync_playwright

output_dir = 'C:/tx_dmv/driving_rule_animations_suite/verification_frames/L05_T03'
os.makedirs(output_dir, exist_ok=True)

sim_path = 'file:///C:/tx_dmv/driving_rule_animations_suite/simulations/L05_T03_signaling_and_communication.html'

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
            if (!el) return null;
            const r = el.getBoundingClientRect();
            const s = window.getComputedStyle(el);
            if (s.opacity === '0' || s.display === 'none' || s.visibility === 'hidden') return null;
            return {{ left: r.left, top: r.top, right: r.right, bottom: r.bottom, width: r.width, height: r.height }};
        }}''')

        box_b = page.evaluate(f'''() => {{
            const el = document.querySelector("{selector_b}");
            if (!el) return null;
            const r = el.getBoundingClientRect();
            const s = window.getComputedStyle(el);
            if (s.opacity === '0' || s.display === 'none' || s.visibility === 'hidden') return null;
            return {{ left: r.left, top: r.top, right: r.right, bottom: r.bottom, width: r.width, height: r.height }};
        }}''')

        if not box_a or not box_b:
            return False, box_a, box_b

        overlap = not (
            box_a['right'] <= box_b['left'] or
            box_a['left'] >= box_b['right'] or
            box_a['bottom'] <= box_b['top'] or
            box_a['top'] >= box_b['bottom']
        )
        return overlap, box_a, box_b

    # Pause playback
    page.evaluate("isPlaying = false;")

    # TEST 1: Step 1 Approach Corridor (150 FT, t = 0.8s)
    print("=== TEST 1: Step 1 Approach Corridor (t = 0.8s) ===")
    page.click("button[data-step='1']")
    page.wait_for_timeout(200)
    page.screenshot(path=os.path.join(output_dir, "step1_approach_corridor_150ft.png"))
    tag_ov, b1, b2 = check_overlap("#tag-veh-ego", "#tag-veh-trail")
    veh_ov, v1, v2 = check_overlap("#veh-ego-container", "#veh-trail-container")
    card_ov, _, _ = check_overlap("#telemetry-hud-card", "#tag-veh-ego")
    pill_ov, _, _ = check_overlap("#hud-status-pill", "#telemetry-hud-card")
    print(f"Step 1 Overlaps: Tags: {tag_ov}, Vehicles: {veh_ov}, Card/Tag: {card_ov}, Pill/Card: {pill_ov}")

    # TEST 2: Step 2 100-FT Statutory Trigger (t = 2.2s)
    print("=== TEST 2: Step 2 100-FT Statutory Trigger (t = 2.2s) ===")
    page.click("button[data-step='2']")
    page.wait_for_timeout(200)
    page.screenshot(path=os.path.join(output_dir, "step2_statutory_100ft_trigger.png"))
    tag_ov, b1, b2 = check_overlap("#tag-veh-ego", "#tag-veh-trail")
    veh_ov, v1, v2 = check_overlap("#veh-ego-container", "#veh-trail-container")
    card_ov, _, _ = check_overlap("#telemetry-hud-card", "#tag-veh-ego")
    print(f"Step 2 Overlaps: Tags: {tag_ov}, Vehicles: {veh_ov}, Card/Tag: {card_ov}")

    # TEST 3: Step 3 Continuous Signal & Decel (t = 4.2s)
    print("=== TEST 3: Step 3 Continuous Signal & Decel (t = 4.2s) ===")
    page.click("button[data-step='3']")
    page.wait_for_timeout(200)
    page.screenshot(path=os.path.join(output_dir, "step3_continuous_signal_and_decel.png"))
    tag_ov, b1, b2 = check_overlap("#tag-veh-ego", "#tag-veh-trail")
    veh_ov, v1, v2 = check_overlap("#veh-ego-container", "#veh-trail-container")
    card_ov, _, _ = check_overlap("#telemetry-hud-card", "#tag-veh-ego")
    print(f"Step 3 Overlaps: Tags: {tag_ov}, Vehicles: {veh_ov}, Card/Tag: {card_ov}")

    # TEST 4: Step 4 Turn Execution & Auto-Cancel (t = 6.8s)
    print("=== TEST 4: Step 4 Turn Execution (t = 6.8s) ===")
    page.click("button[data-step='4']")
    page.wait_for_timeout(200)
    page.screenshot(path=os.path.join(output_dir, "step4_turn_execution_and_autocancel.png"))
    tag_ov, b1, b2 = check_overlap("#tag-veh-ego", "#tag-veh-trail")
    veh_ov, v1, v2 = check_overlap("#veh-ego-container", "#veh-trail-container")
    card_ov, _, _ = check_overlap("#telemetry-hud-card", "#tag-veh-ego")
    print(f"Step 4 Overlaps: Tags: {tag_ov}, Vehicles: {veh_ov}, Card/Tag: {card_ov}")

    # TEST 5: Mode 2 Lane Change Advance Signal (t = 2.5s)
    print("=== TEST 5: Mode 2 Lane Change Advance Signal (t = 2.5s) ===")
    page.click("#mode-btn-2")
    page.wait_for_timeout(200)
    page.click("button[data-step='2']")
    page.wait_for_timeout(200)
    page.screenshot(path=os.path.join(output_dir, "mode2_lane_change_100ft_advance_signal.png"))
    tag_ov, b1, b2 = check_overlap("#tag-veh-ego", "#tag-veh-trail")
    veh_ov, v1, v2 = check_overlap("#veh-ego-container", "#veh-trail-container")
    card_ov, _, _ = check_overlap("#telemetry-hud-card", "#tag-veh-ego")
    print(f"Mode 2 Overlaps: Tags: {tag_ov}, Vehicles: {veh_ov}, Card/Tag: {card_ov}")

    # TEST 6: Mode 3 Hazard Demo Sudden Turn Without Signal (t = 3.4s)
    print("=== TEST 6: Mode 3 Hazard Demo Sudden Turn Without Signal (t = 3.4s) ===")
    page.click("#mode-btn-3")
    page.wait_for_timeout(200)
    page.click("button[data-step='3']")
    page.wait_for_timeout(200)
    page.screenshot(path=os.path.join(output_dir, "mode3_hazard_sudden_turn_rear_end_collision.png"))
    banner_hud_ov, _, _ = check_overlap("#hazard-banner", "#telemetry-hud-card")
    banner_pill_ov, _, _ = check_overlap("#hazard-banner", "#hud-status-pill")
    print(f"Mode 3 Overlap: Banner/HUD: {banner_hud_ov}, Banner/Pill: {banner_pill_ov}")

    print("\n=== CONSOLE LOGS & ERRORS ===")
    print(f"Total Console Logs: {len(console_logs)}")
    for log in console_logs:
        print(f"   {log}")
    print(f"Total JS Errors: {len(js_errors)}")
    for err in js_errors:
        print(f"   ERROR: {err}")

    browser.close()

print("Lesson 12 verification and capture complete!")
