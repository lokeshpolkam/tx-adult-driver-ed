import os
import sys
from playwright.sync_api import sync_playwright

def test_l05_t11():
    html_path = os.path.abspath('driving_rule_animations_suite/simulations/L05_T11_freeway_entry_exit.html')
    output_dir = os.path.abspath('driving_rule_animations_suite/verification_frames/L05_T11')
    os.makedirs(output_dir, exist_ok=True)

    console_logs = []
    js_errors = []

    def handle_console(msg):
        console_logs.append(f"[{msg.type}] {msg.text}")
        if msg.type == 'error':
            js_errors.append(msg.text)

    def check_overlap(b1, b2, margin=2):
        if not b1 or not b2:
            return False
        return not (
            b1['x'] + b1['width'] - margin <= b2['x'] or
            b2['x'] + b2['width'] - margin <= b1['x'] or
            b1['y'] + b1['height'] - margin <= b2['y'] or
            b2['y'] + b2['height'] - margin <= b1['y']
        )

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1280, 'height': 720})

        page.on('console', handle_console)
        page.on('pageerror', lambda err: js_errors.append(str(err)))

        page.goto(f"file:///{html_path}")
        page.wait_for_timeout(500)

        # -------------------------------------------------------------
        # TEST 1: Step 1 Ramp Evaluation (t = 0.8s)
        # -------------------------------------------------------------
        print("=== TEST 1: Step 1 Ramp Evaluation (t = 0.8s) ===")
        page.click("button[data-step='1']")
        page.wait_for_timeout(300)

        hud_box = page.locator("#telemetry-hud-card").bounding_box()
        ego_tag_box = page.locator("#tag-veh-ego").bounding_box()
        pill_box = page.locator("#hud-status-pill").bounding_box()
        lead_tag_box = page.locator("#tag-veh-lead").bounding_box()
        trail_tag_box = page.locator("#tag-veh-trail").bounding_box()

        overlap_hud_ego = check_overlap(hud_box, ego_tag_box)
        overlap_pill_hud = check_overlap(pill_box, hud_box)
        overlap_ego_trail = check_overlap(ego_tag_box, trail_tag_box)
        overlap_ego_lead = check_overlap(ego_tag_box, lead_tag_box)
        print(f"Step 1 Overlaps: HUD/Ego: {overlap_hud_ego}, Pill/HUD: {overlap_pill_hud}, Ego/Trail: {overlap_ego_trail}, Ego/Lead: {overlap_ego_lead}")
        assert not overlap_hud_ego, "HUD overlaps Ego tag in Step 1!"
        assert not overlap_pill_hud, "Pill overlaps HUD in Step 1!"
        assert not overlap_ego_trail, "Ego tag overlaps Trail tag in Step 1!"

        frame1_path = os.path.join(output_dir, "frame_01_step1_ramp_curve.png")
        page.screenshot(path=frame1_path)
        print(f"Saved: {frame1_path}")

        # -------------------------------------------------------------
        # TEST 2: Step 2 Acceleration Runway (t = 2.2s)
        # -------------------------------------------------------------
        print("\n=== TEST 2: Step 2 Acceleration Runway (t = 2.2s) ===")
        page.click("button[data-step='2']")
        page.wait_for_timeout(300)

        ego_tag_box = page.locator("#tag-veh-ego").bounding_box()
        lead_tag_box = page.locator("#tag-veh-lead").bounding_box()
        trail_tag_box = page.locator("#tag-veh-trail").bounding_box()

        overlap_ego_lead = check_overlap(ego_tag_box, lead_tag_box)
        overlap_ego_trail = check_overlap(ego_tag_box, trail_tag_box)
        overlap_lead_trail = check_overlap(lead_tag_box, trail_tag_box)
        print(f"Step 2 Tag Overlaps: Ego/Lead: {overlap_ego_lead}, Ego/Trail: {overlap_ego_trail}, Lead/Trail: {overlap_lead_trail}")
        assert not overlap_ego_lead, "Ego tag overlaps Lead tag in Step 2!"
        assert not overlap_ego_trail, "Ego tag overlaps Trail tag in Step 2!"
        assert not overlap_lead_trail, "Lead tag overlaps Trail tag in Step 2!"

        frame2_path = os.path.join(output_dir, "frame_02_step2_acceleration_runway.png")
        page.screenshot(path=frame2_path)
        print(f"Saved: {frame2_path}")

        # -------------------------------------------------------------
        # TEST 3: Step 3 Speed-Matched Merge (t = 3.6s)
        # -------------------------------------------------------------
        print("\n=== TEST 3: Step 3 Speed-Matched Merge (t = 3.6s) ===")
        page.click("button[data-step='3']")
        page.wait_for_timeout(300)

        ego_tag_box = page.locator("#tag-veh-ego").bounding_box()
        lead_tag_box = page.locator("#tag-veh-lead").bounding_box()
        trail_tag_box = page.locator("#tag-veh-trail").bounding_box()

        overlap_ego_lead = check_overlap(ego_tag_box, lead_tag_box)
        overlap_ego_trail = check_overlap(ego_tag_box, trail_tag_box)
        print(f"Step 3 Tag Overlaps: Ego/Lead: {overlap_ego_lead}, Ego/Trail: {overlap_ego_trail}")
        assert not overlap_ego_lead, "Ego tag overlaps Lead tag in Step 3!"
        assert not overlap_ego_trail, "Ego tag overlaps Trail tag in Step 3!"

        frame3_path = os.path.join(output_dir, "frame_03_step3_speed_matched_merge.png")
        page.screenshot(path=frame3_path)
        print(f"Saved: {frame3_path}")

        # -------------------------------------------------------------
        # TEST 4: Step 4 Mainlane Established Cushion (t = 5.0s)
        # -------------------------------------------------------------
        print("\n=== TEST 4: Step 4 Mainlane Established Cushion (t = 5.0s) ===")
        page.click("button[data-step='4']")
        page.wait_for_timeout(300)

        ego_tag_box = page.locator("#tag-veh-ego").bounding_box()
        lead_tag_box = page.locator("#tag-veh-lead").bounding_box()
        trail_tag_box = page.locator("#tag-veh-trail").bounding_box()

        overlap_ego_lead = check_overlap(ego_tag_box, lead_tag_box)
        overlap_ego_trail = check_overlap(ego_tag_box, trail_tag_box)
        print(f"Step 4 Tag Overlaps: Ego/Lead: {overlap_ego_lead}, Ego/Trail: {overlap_ego_trail}")
        assert not overlap_ego_lead, "Ego tag overlaps Lead tag in Step 4!"
        assert not overlap_ego_trail, "Ego tag overlaps Trail tag in Step 4!"

        frame4_path = os.path.join(output_dir, "frame_04_step4_mainlane_buffer.png")
        page.screenshot(path=frame4_path)
        print(f"Saved: {frame4_path}")

        # -------------------------------------------------------------
        # TEST 5: Mode 2 Freeway Exit & Deceleration Lane (t = 2.2s)
        # -------------------------------------------------------------
        print("\n=== TEST 5: Mode 2 Freeway Exit & Deceleration Lane ===")
        page.click("#mode-btn-2")
        page.wait_for_timeout(300)
        page.click("button[data-step='2']")
        page.wait_for_timeout(300)

        ego_tag_box = page.locator("#tag-veh-ego").bounding_box()
        hud_box = page.locator("#telemetry-hud-card").bounding_box()
        trail_tag_box = page.locator("#tag-veh-trail").bounding_box()
        overlap_ego_hud = check_overlap(ego_tag_box, hud_box)
        overlap_ego_trail = check_overlap(ego_tag_box, trail_tag_box)
        print(f"Mode 2 Ego/HUD Overlap: {overlap_ego_hud}, Ego/Trail Overlap: {overlap_ego_trail}")
        assert not overlap_ego_hud, "Ego tag overlaps HUD in Mode 2!"
        assert not overlap_ego_trail, "Ego tag overlaps Trail tag in Mode 2!"

        frame5_path = os.path.join(output_dir, "frame_05_mode2_decel_exit.png")
        page.screenshot(path=frame5_path)
        print(f"Saved: {frame5_path}")

        # -------------------------------------------------------------
        # TEST 6: Mode 3 Dead Stop Ramp Hazard (t = 3.6s)
        # -------------------------------------------------------------
        print("\n=== TEST 6: Mode 3 Dead Stop Ramp Hazard ===")
        page.click("#mode-btn-3")
        page.wait_for_timeout(300)
        page.click("button[data-step='3']")
        page.wait_for_timeout(300)

        trail_tag_box = page.locator("#tag-veh-trail").bounding_box()
        ego_tag_box = page.locator("#tag-veh-ego").bounding_box()
        banner_box = page.locator("#hazard-banner").bounding_box()
        hud_box = page.locator("#telemetry-hud-card").bounding_box()
        pill_box = page.locator("#hud-status-pill").bounding_box()

        overlap_ego_trail = check_overlap(ego_tag_box, trail_tag_box)
        overlap_banner_hud = check_overlap(banner_box, hud_box)
        overlap_banner_pill = check_overlap(banner_box, pill_box)
        overlap_banner_ego = check_overlap(banner_box, ego_tag_box)
        print(f"Mode 3 Ego/Trail Overlap: {overlap_ego_trail}, Banner/HUD: {overlap_banner_hud}, Banner/Pill: {overlap_banner_pill}, Banner/Ego: {overlap_banner_ego}")
        assert not overlap_ego_trail, "Ego tag overlaps Trail tag in Mode 3!"
        assert not overlap_banner_hud, "Hazard banner overlaps HUD in Mode 3!"
        assert not overlap_banner_pill, "Hazard banner overlaps Pill in Mode 3!"
        assert not overlap_banner_ego, "Hazard banner overlaps Ego in Mode 3!"

        frame6_path = os.path.join(output_dir, "frame_06_mode3_ramp_stop_hazard.png")
        page.screenshot(path=frame6_path)
        print(f"Saved: {frame6_path}")

        browser.close()

    print("\n================ VERIFICATION SUMMARY ================")
    print(f"Total JS Errors: {len(js_errors)}")
    for err in js_errors:
        print(f"  - ERROR: {err}")
    if js_errors:
        sys.exit(1)
    else:
        print("ALL PLAYWRIGHT ASSERTIONS PASSED WITH 0 ERRORS.")

if __name__ == "__main__":
    test_l05_t11()
