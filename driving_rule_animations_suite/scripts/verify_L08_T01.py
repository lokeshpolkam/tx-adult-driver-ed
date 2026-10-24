import os
import sys
from playwright.sync_api import sync_playwright

def test_l08_t01():
    html_path = os.path.abspath('driving_rule_animations_suite/simulations/L08_T01_sipde_scan_cycle.html')
    output_dir = os.path.abspath('driving_rule_animations_suite/verification_frames/L08_T01')
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
        # TEST 1: Step 1 S - Search (12-15s Horizon) (t = 0.8s)
        # -------------------------------------------------------------
        print("=== TEST 1: Step 1 Search 12-15s Horizon (t = 0.8s) ===")
        page.click("button[data-step='1']")
        page.wait_for_timeout(300)

        hud_box = page.locator("#telemetry-hud-card").bounding_box()
        pill_box = page.locator("#hud-status-pill").bounding_box()
        ego_tag_box = page.locator("#tag-veh-ego").bounding_box()
        yellow_tag_box = page.locator("#tag-veh-yellow").bounding_box()
        blue_tag_box = page.locator("#tag-veh-blue").bounding_box()

        overlap_hud_ego = check_overlap(hud_box, ego_tag_box)
        overlap_pill_hud = check_overlap(pill_box, hud_box)
        overlap_ego_yellow = check_overlap(ego_tag_box, yellow_tag_box)
        overlap_ego_blue = check_overlap(ego_tag_box, blue_tag_box)
        overlap_yellow_blue = check_overlap(yellow_tag_box, blue_tag_box)
        print(f"Step 1 Overlaps: HUD/Ego: {overlap_hud_ego}, Pill/HUD: {overlap_pill_hud}, Ego/Yellow: {overlap_ego_yellow}, Ego/Blue: {overlap_ego_blue}, Yellow/Blue: {overlap_yellow_blue}")
        assert not overlap_hud_ego, "HUD overlaps Ego tag in Step 1!"
        assert not overlap_pill_hud, "Pill overlaps HUD in Step 1!"
        assert not overlap_ego_yellow, "Ego tag overlaps Yellow tag in Step 1!"
        assert not overlap_ego_blue, "Ego tag overlaps Blue tag in Step 1!"
        assert not overlap_yellow_blue, "Yellow tag overlaps Blue tag in Step 1!"

        frame1_path = os.path.join(output_dir, "frame_01_step1_search_horizon.png")
        page.screenshot(path=frame1_path)
        print(f"Saved: {frame1_path}")

        # -------------------------------------------------------------
        # TEST 2: Step 2 I & P - Identify & Predict (t = 2.2s)
        # -------------------------------------------------------------
        print("\n=== TEST 2: Step 2 Identify & Predict (t = 2.2s) ===")
        page.click("button[data-step='2']")
        page.wait_for_timeout(300)

        ego_tag_box = page.locator("#tag-veh-ego").bounding_box()
        yellow_tag_box = page.locator("#tag-veh-yellow").bounding_box()
        blue_tag_box = page.locator("#tag-veh-blue").bounding_box()

        overlap_ego_yellow = check_overlap(ego_tag_box, yellow_tag_box)
        overlap_ego_blue = check_overlap(ego_tag_box, blue_tag_box)
        overlap_yellow_blue = check_overlap(yellow_tag_box, blue_tag_box)
        print(f"Step 2 Tag Overlaps: Ego/Yellow: {overlap_ego_yellow}, Ego/Blue: {overlap_ego_blue}, Yellow/Blue: {overlap_yellow_blue}")
        assert not overlap_ego_yellow, "Ego tag overlaps Yellow tag in Step 2!"
        assert not overlap_ego_blue, "Ego tag overlaps Blue tag in Step 2!"
        assert not overlap_yellow_blue, "Yellow tag overlaps Blue tag in Step 2!"

        frame2_path = os.path.join(output_dir, "frame_02_step2_identify_predict.png")
        page.screenshot(path=frame2_path)
        print(f"Saved: {frame2_path}")

        # -------------------------------------------------------------
        # TEST 3: Step 3 D - Decide Space Cushion (t = 3.6s)
        # -------------------------------------------------------------
        print("\n=== TEST 3: Step 3 Decide Space Cushion (t = 3.6s) ===")
        page.click("button[data-step='3']")
        page.wait_for_timeout(300)

        ego_tag_box = page.locator("#tag-veh-ego").bounding_box()
        yellow_tag_box = page.locator("#tag-veh-yellow").bounding_box()
        blue_tag_box = page.locator("#tag-veh-blue").bounding_box()

        overlap_ego_yellow = check_overlap(ego_tag_box, yellow_tag_box)
        overlap_ego_blue = check_overlap(ego_tag_box, blue_tag_box)
        overlap_yellow_blue = check_overlap(yellow_tag_box, blue_tag_box)
        print(f"Step 3 Tag Overlaps: Ego/Yellow: {overlap_ego_yellow}, Ego/Blue: {overlap_ego_blue}, Yellow/Blue: {overlap_yellow_blue}")
        assert not overlap_ego_yellow, "Ego tag overlaps Yellow tag in Step 3!"
        assert not overlap_ego_blue, "Ego tag overlaps Blue tag in Step 3!"
        assert not overlap_yellow_blue, "Yellow tag overlaps Blue tag in Step 3!"

        frame3_path = os.path.join(output_dir, "frame_03_step3_decide_cushion.png")
        page.screenshot(path=frame3_path)
        print(f"Saved: {frame3_path}")

        # -------------------------------------------------------------
        # TEST 4: Step 4 E - Execute 360° Defense (t = 5.0s)
        # -------------------------------------------------------------
        print("\n=== TEST 4: Step 4 Execute 360° Defense (t = 5.0s) ===")
        page.click("button[data-step='4']")
        page.wait_for_timeout(300)

        ego_tag_box = page.locator("#tag-veh-ego").bounding_box()
        yellow_tag_box = page.locator("#tag-veh-yellow").bounding_box()
        blue_tag_box = page.locator("#tag-veh-blue").bounding_box()

        overlap_ego_yellow = check_overlap(ego_tag_box, yellow_tag_box)
        overlap_ego_blue = check_overlap(ego_tag_box, blue_tag_box)
        overlap_yellow_blue = check_overlap(yellow_tag_box, blue_tag_box)
        print(f"Step 4 Tag Overlaps: Ego/Yellow: {overlap_ego_yellow}, Ego/Blue: {overlap_ego_blue}, Yellow/Blue: {overlap_yellow_blue}")
        assert not overlap_ego_yellow, "Ego tag overlaps Yellow tag in Step 4!"
        assert not overlap_ego_blue, "Ego tag overlaps Blue tag in Step 4!"
        assert not overlap_yellow_blue, "Yellow tag overlaps Blue tag in Step 4!"

        frame4_path = os.path.join(output_dir, "frame_04_step4_execute_defense.png")
        page.screenshot(path=frame4_path)
        print(f"Saved: {frame4_path}")

        # -------------------------------------------------------------
        # TEST 5: Scenario 2 - Fixed Gaze Tunnel Vision Hazard
        # -------------------------------------------------------------
        print("\n=== TEST 5: Scenario 2 - Fixed Gaze Tunnel Vision Hazard ===")
        page.click("button[data-mode='2']")
        page.wait_for_timeout(300)

        ego_tag_box = page.locator("#tag-veh-ego").bounding_box()
        yellow_tag_box = page.locator("#tag-veh-yellow").bounding_box()
        hazard_banner_box = page.locator("#hazard-banner").bounding_box()

        overlap_ego_yellow = check_overlap(ego_tag_box, yellow_tag_box)
        overlap_banner_hud = check_overlap(hazard_banner_box, hud_box)
        print(f"Mode 2 Overlaps: Ego/Yellow: {overlap_ego_yellow}, Banner/HUD: {overlap_banner_hud}")
        assert not overlap_ego_yellow, "Ego tag overlaps Yellow tag in Mode 2!"
        assert not overlap_banner_hud, "Hazard banner overlaps HUD in Mode 2!"

        frame5_path = os.path.join(output_dir, "frame_05_mode2_tunnel_vision_hazard.png")
        page.screenshot(path=frame5_path)
        print(f"Saved: {frame5_path}")

        # -------------------------------------------------------------
        # TEST 6: Scenario 3 - Boxed-In No Escape Trap Hazard
        # -------------------------------------------------------------
        print("\n=== TEST 6: Scenario 3 - Boxed-In No Escape Trap Hazard ===")
        page.click("button[data-mode='3']")
        page.wait_for_timeout(300)

        ego_tag_box = page.locator("#tag-veh-ego").bounding_box()
        yellow_tag_box = page.locator("#tag-veh-yellow").bounding_box()
        blue_tag_box = page.locator("#tag-veh-blue").bounding_box()
        hazard_banner_box = page.locator("#hazard-banner").bounding_box()

        overlap_ego_yellow = check_overlap(ego_tag_box, yellow_tag_box)
        overlap_ego_blue = check_overlap(ego_tag_box, blue_tag_box)
        overlap_banner_hud = check_overlap(hazard_banner_box, hud_box)
        print(f"Mode 3 Overlaps: Ego/Yellow: {overlap_ego_yellow}, Ego/Blue: {overlap_ego_blue}, Banner/HUD: {overlap_banner_hud}")
        assert not overlap_ego_yellow, "Ego tag overlaps Yellow tag in Mode 3!"
        assert not overlap_ego_blue, "Ego tag overlaps Blue tag in Mode 3!"
        assert not overlap_banner_hud, "Hazard banner overlaps HUD in Mode 3!"

        frame6_path = os.path.join(output_dir, "frame_06_mode3_boxed_in_hazard.png")
        page.screenshot(path=frame6_path)
        print(f"Saved: {frame6_path}")

        # Check JS Errors
        print(f"\nTotal JS Errors: {len(js_errors)}")
        if js_errors:
            for err in js_errors:
                print(f"JS ERROR: {err}")
        assert len(js_errors) == 0, f"Found {len(js_errors)} JavaScript errors!"

        browser.close()
        print("\n=== ALL L08-T01 VERIFICATION TESTS PASSED SUCCESSFULLY! ===")

if __name__ == '__main__':
    test_l08_t01()
