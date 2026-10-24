import os
import sys
from playwright.sync_api import sync_playwright

def test_l08_t07():
    html_path = os.path.abspath('driving_rule_animations_suite/simulations/L08_T07_night_driving.html')
    output_dir = os.path.abspath('driving_rule_animations_suite/verification_frames/L08_T07')
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
        page = browser.new_page(viewport={'width': 1280, 'height': 960})

        page.on('console', handle_console)
        page.on('pageerror', lambda err: js_errors.append(str(err)))

        page.goto(f"file:///{html_path}")
        page.wait_for_timeout(500)

        # -------------------------------------------------------------
        # TEST 1: Step 1 Low Beam: 45 MPH Safe (t = 1.0s)
        # -------------------------------------------------------------
        print("=== TEST 1: Step 1 Low Beam: 45 MPH Safe ===")
        page.click("button[data-step='1']")
        page.wait_for_timeout(300)

        hud_box = page.locator("#telemetry-hud").bounding_box()
        ego_tag_box = page.locator("#ego-tag").bounding_box()
        yellow_tag_box = page.locator("#yellow-tag").bounding_box()
        widget_box = page.locator("#lighting-widget").bounding_box()

        assert not check_overlap(hud_box, ego_tag_box), "HUD overlaps Ego tag in Step 1!"
        assert not check_overlap(ego_tag_box, yellow_tag_box), "Ego tag overlaps Yellow tag in Step 1!"
        assert not check_overlap(widget_box, yellow_tag_box), "Widget overlaps Yellow tag in Step 1!"

        frame1_path = os.path.join(output_dir, "frame_01_step1_low_beam_safe.png")
        page.screenshot(path=frame1_path)
        print(f"Saved: {frame1_path}")

        # -------------------------------------------------------------
        # TEST 2: Step 2 Speed Surge: Overdriving! (t = 4.5s)
        # -------------------------------------------------------------
        print("\n=== TEST 2: Step 2 Speed Surge: Overdriving! ===")
        page.click("button[data-step='2']")
        page.wait_for_timeout(300)

        hud_box = page.locator("#telemetry-hud").bounding_box()
        ego_tag_box = page.locator("#ego-tag").bounding_box()
        yellow_tag_box = page.locator("#yellow-tag").bounding_box()
        widget_box = page.locator("#lighting-widget").bounding_box()

        assert not check_overlap(hud_box, ego_tag_box), "HUD overlaps Ego tag in Step 2!"
        assert not check_overlap(ego_tag_box, yellow_tag_box), "Ego tag overlaps Yellow tag in Step 2!"
        assert not check_overlap(widget_box, yellow_tag_box), "Widget overlaps Yellow tag in Step 2!"

        frame2_path = os.path.join(output_dir, "frame_02_step2_speed_overdrive.png")
        page.screenshot(path=frame2_path)
        print(f"Saved: {frame2_path}")

        # -------------------------------------------------------------
        # TEST 3: Step 3 Unlit Obstacle in Dark (t = 7.5s)
        # -------------------------------------------------------------
        print("\n=== TEST 3: Step 3 Unlit Obstacle in Dark ===")
        page.click("button[data-step='3']")
        page.wait_for_timeout(300)

        hud_box = page.locator("#telemetry-hud").bounding_box()
        ego_tag_box = page.locator("#ego-tag").bounding_box()
        yellow_tag_box = page.locator("#yellow-tag").bounding_box()
        widget_box = page.locator("#lighting-widget").bounding_box()

        assert not check_overlap(hud_box, ego_tag_box), "HUD overlaps Ego tag in Step 3!"
        assert not check_overlap(ego_tag_box, yellow_tag_box), "Ego tag overlaps Yellow tag in Step 3!"
        assert not check_overlap(widget_box, yellow_tag_box), "Widget overlaps Yellow tag in Step 3!"

        frame3_path = os.path.join(output_dir, "frame_03_step3_unlit_obstacle.png")
        page.screenshot(path=frame3_path)
        print(f"Saved: {frame3_path}")

        # -------------------------------------------------------------
        # TEST 4: Step 4 High Beam or Slower Speed (t = 10.5s)
        # -------------------------------------------------------------
        print("\n=== TEST 4: Step 4 High Beam or Slower Speed ===")
        page.click("button[data-step='4']")
        page.wait_for_timeout(300)

        hud_box = page.locator("#telemetry-hud").bounding_box()
        ego_tag_box = page.locator("#ego-tag").bounding_box()
        yellow_tag_box = page.locator("#yellow-tag").bounding_box()

        assert not check_overlap(hud_box, ego_tag_box), "HUD overlaps Ego tag in Step 4!"
        assert not check_overlap(ego_tag_box, yellow_tag_box), "Ego tag overlaps Yellow tag in Step 4!"

        frame4_path = os.path.join(output_dir, "frame_04_step4_high_beam_safe.png")
        page.screenshot(path=frame4_path)
        print(f"Saved: {frame4_path}")

        # -------------------------------------------------------------
        # TEST 5: Mode 2 Glare & 500-FT Dimming Hazard
        # -------------------------------------------------------------
        print("\n=== TEST 5: Mode 2 Glare & 500-FT Dimming Hazard ===")
        page.click("#mode-2")
        page.wait_for_timeout(400)

        hud_box = page.locator("#telemetry-hud").bounding_box()
        banner_box = page.locator("#hazard-banner").bounding_box()
        ego_tag_box = page.locator("#ego-tag").bounding_box()
        yellow_tag_box = page.locator("#yellow-tag").bounding_box()
        widget_box = page.locator("#lighting-widget").bounding_box()

        assert not check_overlap(hud_box, banner_box), "HUD overlaps Hazard Banner in Mode 2!"
        assert not check_overlap(hud_box, ego_tag_box), "HUD overlaps Ego tag in Mode 2!"
        assert not check_overlap(ego_tag_box, yellow_tag_box), "Ego tag overlaps Oncoming car tag in Mode 2!"
        assert not check_overlap(banner_box, ego_tag_box), "Hazard Banner overlaps Ego tag in Mode 2!"
        assert not check_overlap(banner_box, yellow_tag_box), "Hazard Banner overlaps Yellow tag in Mode 2!"
        assert not check_overlap(banner_box, widget_box), "Hazard Banner overlaps Widget in Mode 2!"

        frame5_path = os.path.join(output_dir, "frame_05_mode2_oncoming_glare.png")
        page.screenshot(path=frame5_path)
        print(f"Saved: {frame5_path}")

        # -------------------------------------------------------------
        # TEST 6: Mode 3 300-FT Following Dimming Mandate
        # -------------------------------------------------------------
        print("\n=== TEST 6: Mode 3 300-FT Following Dimming Mandate ===")
        page.click("#mode-3")
        page.wait_for_timeout(400)

        hud_box = page.locator("#telemetry-hud").bounding_box()
        banner_box = page.locator("#hazard-banner").bounding_box()
        ego_tag_box = page.locator("#ego-tag").bounding_box()
        yellow_tag_box = page.locator("#yellow-tag").bounding_box()
        widget_box = page.locator("#lighting-widget").bounding_box()

        assert not check_overlap(hud_box, banner_box), "HUD overlaps Hazard Banner in Mode 3!"
        assert not check_overlap(ego_tag_box, yellow_tag_box), "Ego tag overlaps Lead car tag in Mode 3!"
        assert not check_overlap(banner_box, yellow_tag_box), "Hazard Banner overlaps Lead car tag in Mode 3!"
        assert not check_overlap(banner_box, ego_tag_box), "Hazard Banner overlaps Ego tag in Mode 3!"
        assert not check_overlap(banner_box, widget_box), "Hazard Banner overlaps Widget in Mode 3!"

        frame6_path = os.path.join(output_dir, "frame_06_mode3_rear_dimming.png")
        page.screenshot(path=frame6_path)
        print(f"Saved: {frame6_path}")

        # -------------------------------------------------------------
        # VERIFY CONSOLE ERRORS
        # -------------------------------------------------------------
        print("\n=== VERIFYING CONSOLE LOGS & JS ERRORS ===")
        print(f"Total Console logs: {len(console_logs)}")
        print(f"Total JS Errors: {len(js_errors)}")
        if js_errors:
            print(f"CRITICAL ERROR: JS Errors encountered: {js_errors}")
            sys.exit(1)

        print("\nALL 6 PLAYWRIGHT TESTS PASSED WITH ZERO CONSOLE ERRORS AND ZERO TAG OVERLAPS!")
        browser.close()

if __name__ == '__main__':
    test_l08_t07()
