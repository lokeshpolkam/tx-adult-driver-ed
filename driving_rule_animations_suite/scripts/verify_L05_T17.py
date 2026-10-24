import os
import sys
from playwright.sync_api import sync_playwright

def test_l05_t17():
    html_path = os.path.abspath('driving_rule_animations_suite/simulations/L05_T17_work_zones.html')
    output_dir = os.path.abspath('driving_rule_animations_suite/verification_frames/L05_T17')
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
        page = browser.new_page(viewport={'width': 1280, 'height': 840})

        page.on('console', handle_console)
        page.on('pageerror', lambda err: js_errors.append(str(err)))

        page.goto(f"file:///{html_path}")
        page.wait_for_timeout(500)

        # -------------------------------------------------------------
        # TEST 1: Step 1 Advance Warning Signage (t = 0.8s)
        # -------------------------------------------------------------
        print("=== TEST 1: Step 1 Advance Warning Signage (t = 0.8s) ===")
        page.click("button[data-step='1']")
        page.wait_for_timeout(300)

        hud_box = page.locator("#telemetry-hud-card").bounding_box()
        ego_tag_box = page.locator("#tag-veh-ego").bounding_box()
        pill_box = page.locator("#hud-status-pill").bounding_box()
        blue_tag_box = page.locator("#tag-veh-blue").bounding_box()
        yellow_tag_box = page.locator("#tag-veh-yellow").bounding_box()

        overlap_hud_ego = check_overlap(hud_box, ego_tag_box)
        overlap_pill_hud = check_overlap(pill_box, hud_box)
        overlap_ego_yellow = check_overlap(ego_tag_box, yellow_tag_box)
        overlap_ego_blue = check_overlap(ego_tag_box, blue_tag_box)
        print(f"Step 1 Overlaps: HUD/Ego: {overlap_hud_ego}, Pill/HUD: {overlap_pill_hud}, Ego/Yellow: {overlap_ego_yellow}, Ego/Blue: {overlap_ego_blue}")
        assert not overlap_hud_ego, "HUD overlaps Ego tag in Step 1!"
        assert not overlap_pill_hud, "Pill overlaps HUD in Step 1!"
        assert not overlap_ego_yellow, "Ego tag overlaps Yellow tag in Step 1!"
        assert not overlap_ego_blue, "Ego tag overlaps Blue tag in Step 1!"

        frame1_path = os.path.join(output_dir, "frame_01_step1_advance_warning.png")
        page.screenshot(path=frame1_path)
        print(f"Saved: {frame1_path}")

        # -------------------------------------------------------------
        # TEST 2: Step 2 Barrel Taper Merge (t = 2.2s)
        # -------------------------------------------------------------
        print("\n=== TEST 2: Step 2 Barrel Taper Merge (t = 2.2s) ===")
        page.click("button[data-step='2']")
        page.wait_for_timeout(300)

        ego_tag_box = page.locator("#tag-veh-ego").bounding_box()
        blue_tag_box = page.locator("#tag-veh-blue").bounding_box()
        yellow_tag_box = page.locator("#tag-veh-yellow").bounding_box()

        overlap_ego_blue = check_overlap(ego_tag_box, blue_tag_box)
        overlap_ego_yellow = check_overlap(ego_tag_box, yellow_tag_box)
        print(f"Step 2 Tag Overlaps: Ego/Blue: {overlap_ego_blue}, Ego/Yellow: {overlap_ego_yellow}")
        assert not overlap_ego_blue, "Ego tag overlaps Blue tag in Step 2!"
        assert not overlap_ego_yellow, "Ego tag overlaps Yellow tag in Step 2!"

        frame2_path = os.path.join(output_dir, "frame_02_step2_barrel_taper_merge.png")
        page.screenshot(path=frame2_path)
        print(f"Saved: {frame2_path}")

        # -------------------------------------------------------------
        # TEST 3: Step 3 Flagger & Crew Buffer Zone (t = 3.6s)
        # -------------------------------------------------------------
        print("\n=== TEST 3: Step 3 Flagger & Crew Buffer Zone (t = 3.6s) ===")
        page.click("button[data-step='3']")
        page.wait_for_timeout(300)

        ego_tag_box = page.locator("#tag-veh-ego").bounding_box()
        blue_tag_box = page.locator("#tag-veh-blue").bounding_box()
        yellow_tag_box = page.locator("#tag-veh-yellow").bounding_box()

        overlap_ego_blue = check_overlap(ego_tag_box, blue_tag_box)
        overlap_ego_yellow = check_overlap(ego_tag_box, yellow_tag_box)
        print(f"Step 3 Tag Overlaps: Ego/Blue: {overlap_ego_blue}, Ego/Yellow: {overlap_ego_yellow}")
        assert not overlap_ego_blue, "Ego tag overlaps Blue tag in Step 3!"
        assert not overlap_ego_yellow, "Ego tag overlaps Yellow tag in Step 3!"

        frame3_path = os.path.join(output_dir, "frame_03_step3_crew_buffer_zone.png")
        page.screenshot(path=frame3_path)
        print(f"Saved: {frame3_path}")

        # -------------------------------------------------------------
        # TEST 4: Step 4 Safe Work Zone Clearance (t = 5.0s)
        # -------------------------------------------------------------
        print("\n=== TEST 4: Step 4 Safe Work Zone Clearance (t = 5.0s) ===")
        page.click("button[data-step='4']")
        page.wait_for_timeout(300)

        ego_tag_box = page.locator("#tag-veh-ego").bounding_box()
        blue_tag_box = page.locator("#tag-veh-blue").bounding_box()
        yellow_tag_box = page.locator("#tag-veh-yellow").bounding_box()

        overlap_ego_blue = check_overlap(ego_tag_box, blue_tag_box)
        overlap_ego_yellow = check_overlap(ego_tag_box, yellow_tag_box)
        print(f"Step 4 Tag Overlaps: Ego/Blue: {overlap_ego_blue}, Ego/Yellow: {overlap_ego_yellow}")
        assert not overlap_ego_blue, "Ego tag overlaps Blue tag in Step 4!"
        assert not overlap_ego_yellow, "Ego tag overlaps Yellow tag in Step 4!"

        frame4_path = os.path.join(output_dir, "frame_04_step4_clearance_safe.png")
        page.screenshot(path=frame4_path)
        print(f"Saved: {frame4_path}")

        # -------------------------------------------------------------
        # TEST 5: Mode 2 Human Flagger Control (t = 1.8s)
        # -------------------------------------------------------------
        print("\n=== TEST 5: Mode 2 Human Flagger Control ===")
        page.click("#mode-btn-2")
        page.wait_for_timeout(300)
        page.click("button[data-step='2']")
        page.wait_for_timeout(300)

        ego_tag_box = page.locator("#tag-veh-ego").bounding_box()
        hud_box = page.locator("#telemetry-hud-card").bounding_box()
        blue_tag_box = page.locator("#tag-veh-blue").bounding_box()
        yellow_tag_box = page.locator("#tag-veh-yellow").bounding_box()

        overlap_ego_hud = check_overlap(ego_tag_box, hud_box)
        overlap_ego_blue = check_overlap(ego_tag_box, blue_tag_box)
        overlap_ego_yellow = check_overlap(ego_tag_box, yellow_tag_box)
        print(f"Mode 2 Overlaps: Ego/HUD: {overlap_ego_hud}, Ego/Blue: {overlap_ego_blue}, Ego/Yellow: {overlap_ego_yellow}")
        assert not overlap_ego_hud, "Ego tag overlaps HUD in Mode 2!"
        assert not overlap_ego_blue, "Ego tag overlaps Blue tag in Mode 2!"
        assert not overlap_ego_yellow, "Ego tag overlaps Yellow tag in Mode 2!"

        frame5_path = os.path.join(output_dir, "frame_05_mode2_flagger_stop_taper.png")
        page.screenshot(path=frame5_path)
        print(f"Saved: {frame5_path}")

        # -------------------------------------------------------------
        # TEST 6: Mode 3 Work Zone Speeding Hazard (t = 3.6s)
        # -------------------------------------------------------------
        print("\n=== TEST 6: Mode 3 Work Zone Speeding Hazard ===")
        page.click("#mode-btn-3")
        page.wait_for_timeout(300)
        page.click("button[data-step='3']")
        page.wait_for_timeout(300)

        yellow_tag_box = page.locator("#tag-veh-yellow").bounding_box()
        ego_tag_box = page.locator("#tag-veh-ego").bounding_box()
        banner_box = page.locator("#hazard-banner").bounding_box()
        hud_box = page.locator("#telemetry-hud-card").bounding_box()
        pill_box = page.locator("#hud-status-pill").bounding_box()
        blue_tag_box = page.locator("#tag-veh-blue").bounding_box()

        overlap_banner_hud = check_overlap(banner_box, hud_box)
        overlap_banner_pill = check_overlap(banner_box, pill_box)
        overlap_banner_blue = check_overlap(banner_box, blue_tag_box)
        overlap_banner_ego = check_overlap(banner_box, ego_tag_box)
        print(f"Mode 3 Overlaps: Banner/HUD: {overlap_banner_hud}, Banner/Pill: {overlap_banner_pill}, Banner/Blue: {overlap_banner_blue}, Banner/Ego: {overlap_banner_ego}")
        assert not overlap_banner_hud, "Hazard banner overlaps HUD in Mode 3!"
        assert not overlap_banner_pill, "Hazard banner overlaps Pill in Mode 3!"
        assert not overlap_banner_blue, "Hazard banner overlaps Blue tag in Mode 3!"
        assert not overlap_banner_ego, "Hazard banner overlaps Ego tag in Mode 3!"

        frame6_path = os.path.join(output_dir, "frame_06_mode3_speeding_cones_crash.png")
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
    test_l05_t17()
