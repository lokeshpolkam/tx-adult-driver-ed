import os
import json
from playwright.sync_api import sync_playwright

output_dir = 'C:/tx_dmv/driving_rule_animations_suite/verification_frames/L05_T05'
os.makedirs(output_dir, exist_ok=True)

sim_path = 'file:///C:/tx_dmv/driving_rule_animations_suite/simulations/L05_T05_blind_spot_driving.html'

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

    # TEST 1: Step 1 Mirror Cone vs. Blind Spot (t = 0.8s)
    print("=== TEST 1: Step 1 Mirror Cone vs. Blind Spot (t = 0.8s) ===")
    page.click("button[data-step='1']")
    page.wait_for_timeout(200)
    page.screenshot(path=os.path.join(output_dir, "step1_mirror_cone_vs_blind_spot.png"))
    tag_ov_eb, _, _ = check_overlap("#tag-veh-ego", "#tag-veh-blue")
    tag_ov_ey, _, _ = check_overlap("#tag-veh-ego", "#tag-veh-yellow")
    veh_ov_eb, _, _ = check_overlap("#veh-ego-container", "#veh-blue-container")
    veh_ov_ey, _, _ = check_overlap("#veh-ego-container", "#veh-yellow-container")
    card_ov, _, _ = check_overlap("#telemetry-hud-card", "#tag-veh-ego")
    pill_card_ov, _, _ = check_overlap("#hud-status-pill", "#telemetry-hud-card")
    print(f"Step 1 Overlaps: Tags: EB={tag_ov_eb}, EY={tag_ov_ey} | Veh: EB={veh_ov_eb}, EY={veh_ov_ey} | Card/Tag: {card_ov}, Pill/Card: {pill_card_ov}")

    # TEST 2: Step 2 100-Ft Signal & Mirror Check (t = 2.5s)
    print("=== TEST 2: Step 2 100-Ft Signal & Mirror Check (t = 2.5s) ===")
    page.click("button[data-step='2']")
    page.wait_for_timeout(200)
    page.screenshot(path=os.path.join(output_dir, "step2_turn_signal_and_mirror_check.png"))
    tag_ov_eb, _, _ = check_overlap("#tag-veh-ego", "#tag-veh-blue")
    tag_ov_ey, _, _ = check_overlap("#tag-veh-ego", "#tag-veh-yellow")
    veh_ov_eb, _, _ = check_overlap("#veh-ego-container", "#veh-blue-container")
    veh_ov_ey, _, _ = check_overlap("#veh-ego-container", "#veh-yellow-container")
    card_ov, _, _ = check_overlap("#telemetry-hud-card", "#tag-veh-ego")
    print(f"Step 2 Overlaps: Tags: EB={tag_ov_eb}, EY={tag_ov_ey} | Veh: EB={veh_ov_eb}, EY={veh_ov_ey} | Card/Tag: {card_ov}")

    # TEST 3: Step 3 Chin-to-Shoulder Head-Check (t = 4.5s)
    print("=== TEST 3: Step 3 Chin-to-Shoulder Head-Check (t = 4.5s) ===")
    page.click("button[data-step='3']")
    page.wait_for_timeout(200)
    page.screenshot(path=os.path.join(output_dir, "step3_chin_to_shoulder_head_check.png"))
    tag_ov_eb, _, _ = check_overlap("#tag-veh-ego", "#tag-veh-blue")
    veh_ov_eb, _, _ = check_overlap("#veh-ego-container", "#veh-blue-container")
    card_ov, _, _ = check_overlap("#telemetry-hud-card", "#tag-veh-ego")
    print(f"Step 3 Overlaps: Tags: EB={tag_ov_eb} | Veh: EB={veh_ov_eb} | Card/Tag: {card_ov}")

    # TEST 4: Step 4 Cushion Maintained & Safe Entry (t = 6.5s)
    print("=== TEST 4: Step 4 Cushion Maintained & Safe Entry (t = 6.5s) ===")
    page.click("button[data-step='4']")
    page.wait_for_timeout(200)
    page.screenshot(path=os.path.join(output_dir, "step4_cushion_maintained_and_safe_entry.png"))
    tag_ov_eb, _, _ = check_overlap("#tag-veh-ego", "#tag-veh-blue")
    veh_ov_eb, _, _ = check_overlap("#veh-ego-container", "#veh-blue-container")
    card_ov, _, _ = check_overlap("#telemetry-hud-card", "#tag-veh-ego")
    print(f"Step 4 Overlaps: Tags: EB={tag_ov_eb} | Veh: EB={veh_ov_eb} | Card/Tag: {card_ov}")

    # TEST 5: Mode 2 CMV Commercial No-Zones (t = 2.5s)
    print("=== TEST 5: Mode 2 CMV Commercial No-Zones (t = 2.5s) ===")
    page.click("#mode-btn-2")
    page.wait_for_timeout(200)
    page.click("button[data-step='2']")
    page.wait_for_timeout(200)
    page.screenshot(path=os.path.join(output_dir, "mode2_cmv_commercial_no_zones.png"))
    tag_ov_ec, _, _ = check_overlap("#tag-veh-ego", "#tag-veh-cmv")
    veh_ov_ec, _, _ = check_overlap("#veh-ego-container", "#veh-cmv-container")
    card_ov, _, _ = check_overlap("#telemetry-hud-card", "#tag-veh-ego")
    print(f"Mode 2 Overlaps: Tags: EC={tag_ov_ec} | Veh: EC={veh_ov_ec} | Card/Tag: {card_ov}")

    # TEST 6: Mode 3 Hazard Demo Blind Sideswipe (t = 4.2s)
    print("=== TEST 6: Mode 3 Hazard Demo Blind Sideswipe (t = 4.2s) ===")
    page.click("#mode-btn-3")
    page.wait_for_timeout(200)
    page.click("button[data-step='3']")
    page.wait_for_timeout(200)
    page.screenshot(path=os.path.join(output_dir, "mode3_hazard_blind_sideswipe_collision.png"))
    banner_hud_ov, _, _ = check_overlap("#hazard-banner", "#telemetry-hud-card")
    banner_pill_ov, _, _ = check_overlap("#hazard-banner", "#hud-status-pill")
    banner_comp_ov, _, _ = check_overlap("#hazard-banner", "#compliance-badge")
    print(f"Mode 3 Overlap: Banner/HUD: {banner_hud_ov}, Banner/Pill: {banner_pill_ov}, Banner/Comp: {banner_comp_ov}")

    print("\n=== CONSOLE LOGS & ERRORS ===")
    print(f"Total Console Logs: {len(console_logs)}")
    for log in console_logs:
        print(f"   {log}")
    print(f"Total JS Errors: {len(js_errors)}")
    for err in js_errors:
        print(f"   ERROR: {err}")

    browser.close()

print("Lesson 14 verification and capture complete!")
