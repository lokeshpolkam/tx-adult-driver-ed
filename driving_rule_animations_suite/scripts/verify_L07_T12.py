import os
import sys
from playwright.sync_api import sync_playwright

def test_l07_t12():
    html_path = os.path.abspath('driving_rule_animations_suite/simulations/L07_T12_oversize_vehicles.html')
    output_dir = os.path.abspath('driving_rule_animations_suite/verification_frames/L07_T12')
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
        # TEST 1: Step 1 Detect Pilot Strobes & Wide Deck (t = 0.8s)
        # -------------------------------------------------------------
        print("=== TEST 1: Step 1 Detect Pilot Strobes & Wide Deck (t = 0.8s) ===")
        page.click("button[data-step='1']")
        page.wait_for_timeout(300)

        hud_box = page.locator("#telemetry-hud-card").bounding_box()
        pill_box = page.locator("#hud-status-pill").bounding_box()
        ego_tag_box = page.locator("#tag-veh-ego").bounding_box()
        truck_tag_box = page.locator("#tag-veh-truck").bounding_box()
        pilot_tag_box = page.locator("#tag-veh-pilot").bounding_box()

        overlap_hud_ego = check_overlap(hud_box, ego_tag_box)
        overlap_pill_hud = check_overlap(pill_box, hud_box)
        overlap_ego_truck = check_overlap(ego_tag_box, truck_tag_box)
        overlap_truck_pilot = check_overlap(truck_tag_box, pilot_tag_box)
        print(f"Step 1 Overlaps: HUD/Ego: {overlap_hud_ego}, Pill/HUD: {overlap_pill_hud}, Ego/Truck: {overlap_ego_truck}, Truck/Pilot: {overlap_truck_pilot}")
        assert not overlap_hud_ego, "HUD overlaps Ego tag in Step 1!"
        assert not overlap_pill_hud, "Pill overlaps HUD in Step 1!"
        assert not overlap_ego_truck, "Ego tag overlaps Truck tag in Step 1!"
        assert not overlap_truck_pilot, "Truck tag overlaps Pilot tag in Step 1!"

        frame1_path = os.path.join(output_dir, "frame_01_step1_detect_pilot_strobes.png")
        page.screenshot(path=frame1_path)
        print(f"Saved: {frame1_path}")

        # -------------------------------------------------------------
        # TEST 2: Step 2 Respect Convoy Buffer & Straddle (t = 2.2s)
        # -------------------------------------------------------------
        print("\n=== TEST 2: Step 2 Respect Convoy Buffer & Straddle (t = 2.2s) ===")
        page.click("button[data-step='2']")
        page.wait_for_timeout(300)

        ego_tag_box = page.locator("#tag-veh-ego").bounding_box()
        truck_tag_box = page.locator("#tag-veh-truck").bounding_box()
        pilot_tag_box = page.locator("#tag-veh-pilot").bounding_box()

        overlap_ego_truck = check_overlap(ego_tag_box, truck_tag_box)
        overlap_truck_pilot = check_overlap(truck_tag_box, pilot_tag_box)
        print(f"Step 2 Tag Overlaps: Ego/Truck: {overlap_ego_truck}, Truck/Pilot: {overlap_truck_pilot}")
        assert not overlap_ego_truck, "Ego tag overlaps Truck tag in Step 2!"
        assert not overlap_truck_pilot, "Truck tag overlaps Pilot tag in Step 2!"

        frame2_path = os.path.join(output_dir, "frame_02_step2_respect_convoy_buffer.png")
        page.screenshot(path=frame2_path)
        print(f"Saved: {frame2_path}")

        # -------------------------------------------------------------
        # TEST 3: Step 3 Pass Briskly in Passing Lane 3 (t = 3.6s)
        # -------------------------------------------------------------
        print("\n=== TEST 3: Step 3 Pass Briskly in Passing Lane 3 (t = 3.6s) ===")
        page.click("button[data-step='3']")
        page.wait_for_timeout(300)

        ego_tag_box = page.locator("#tag-veh-ego").bounding_box()
        truck_tag_box = page.locator("#tag-veh-truck").bounding_box()
        pilot_tag_box = page.locator("#tag-veh-pilot").bounding_box()

        overlap_ego_truck = check_overlap(ego_tag_box, truck_tag_box)
        overlap_truck_pilot = check_overlap(truck_tag_box, pilot_tag_box)
        overlap_ego_pilot = check_overlap(ego_tag_box, pilot_tag_box)
        print(f"Step 3 Tag Overlaps: Ego/Truck: {overlap_ego_truck}, Truck/Pilot: {overlap_truck_pilot}, Ego/Pilot: {overlap_ego_pilot}")
        assert not overlap_ego_truck, "Ego tag overlaps Truck tag in Step 3!"
        assert not overlap_truck_pilot, "Truck tag overlaps Pilot tag in Step 3!"
        assert not overlap_ego_pilot, "Ego tag overlaps Pilot tag in Step 3!"

        frame3_path = os.path.join(output_dir, "frame_03_step3_pass_in_lane3.png")
        page.screenshot(path=frame3_path)
        print(f"Saved: {frame3_path}")

        # -------------------------------------------------------------
        # TEST 4: Step 4 Mirror Check Headlights Return (t = 5.0s)
        # -------------------------------------------------------------
        print("\n=== TEST 4: Step 4 Mirror Check Headlights Return (t = 5.0s) ===")
        page.click("button[data-step='4']")
        page.wait_for_timeout(300)

        ego_tag_box = page.locator("#tag-veh-ego").bounding_box()
        truck_tag_box = page.locator("#tag-veh-truck").bounding_box()
        pilot_tag_box = page.locator("#tag-veh-pilot").bounding_box()

        overlap_ego_truck = check_overlap(ego_tag_box, truck_tag_box)
        overlap_truck_pilot = check_overlap(truck_tag_box, pilot_tag_box)
        overlap_ego_pilot = check_overlap(ego_tag_box, pilot_tag_box)
        print(f"Step 4 Tag Overlaps: Ego/Truck: {overlap_ego_truck}, Truck/Pilot: {overlap_truck_pilot}, Ego/Pilot: {overlap_ego_pilot}")
        assert not overlap_ego_truck, "Ego tag overlaps Truck tag in Step 4!"
        assert not overlap_truck_pilot, "Truck tag overlaps Pilot tag in Step 4!"
        assert not overlap_ego_pilot, "Ego tag overlaps Pilot tag in Step 4!"

        frame4_path = os.path.join(output_dir, "frame_04_step4_mirror_headlights_check.png")
        page.screenshot(path=frame4_path)
        print(f"Saved: {frame4_path}")

        # -------------------------------------------------------------
        # TEST 5: Scenario 2 - Narrow Bridge Pinch Hazard
        # -------------------------------------------------------------
        print("\n=== TEST 5: Scenario 2 - Narrow Bridge Pinch Hazard ===")
        page.click("button[data-mode='2']")
        page.wait_for_timeout(300)

        ego_tag_box = page.locator("#tag-veh-ego").bounding_box()
        truck_tag_box = page.locator("#tag-veh-truck").bounding_box()
        hazard_banner_box = page.locator("#hazard-banner").bounding_box()

        overlap_ego_truck = check_overlap(ego_tag_box, truck_tag_box)
        overlap_banner_hud = check_overlap(hazard_banner_box, hud_box)
        print(f"Mode 2 Overlaps: Ego/Truck: {overlap_ego_truck}, Banner/HUD: {overlap_banner_hud}")
        assert not overlap_ego_truck, "Ego tag overlaps Truck tag in Mode 2!"
        assert not overlap_banner_hud, "Hazard banner overlaps HUD in Mode 2!"

        frame5_path = os.path.join(output_dir, "frame_05_mode2_narrow_bridge_pinch.png")
        page.screenshot(path=frame5_path)
        print(f"Saved: {frame5_path}")

        # -------------------------------------------------------------
        # TEST 6: Scenario 3 - Premature Cut-In Crush Hazard
        # -------------------------------------------------------------
        print("\n=== TEST 6: Scenario 3 - Premature Cut-In Crush Hazard ===")
        page.click("button[data-mode='3']")
        page.wait_for_timeout(300)

        ego_tag_box = page.locator("#tag-veh-ego").bounding_box()
        truck_tag_box = page.locator("#tag-veh-truck").bounding_box()
        hazard_banner_box = page.locator("#hazard-banner").bounding_box()

        overlap_ego_truck = check_overlap(ego_tag_box, truck_tag_box)
        overlap_banner_hud = check_overlap(hazard_banner_box, hud_box)
        print(f"Mode 3 Overlaps: Ego/Truck: {overlap_ego_truck}, Banner/HUD: {overlap_banner_hud}")
        assert not overlap_ego_truck, "Ego tag overlaps Truck tag in Mode 3!"
        assert not overlap_banner_hud, "Hazard banner overlaps HUD in Mode 3!"

        frame6_path = os.path.join(output_dir, "frame_06_mode3_premature_cutin_crush.png")
        page.screenshot(path=frame6_path)
        print(f"Saved: {frame6_path}")

        # Check JS Errors
        print(f"\nTotal JS Errors: {len(js_errors)}")
        if js_errors:
            for err in js_errors:
                print(f"JS ERROR: {err}")
        assert len(js_errors) == 0, f"Found {len(js_errors)} JavaScript errors!"

        browser.close()
        print("\n=== ALL L07-T12 VERIFICATION TESTS PASSED SUCCESSFULLY! ===")

if __name__ == '__main__':
    test_l07_t12()
