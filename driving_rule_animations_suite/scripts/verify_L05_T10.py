import os
import sys
from playwright.sync_api import sync_playwright

def test_l05_t10():
    html_path = os.path.abspath('driving_rule_animations_suite/simulations/L05_T10_vehicle_lights.html')
    output_dir = os.path.abspath('driving_rule_animations_suite/verification_frames/L05_T10')
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
        # TEST 1: Step 1 High Beams Active (t = 0.8s)
        # -------------------------------------------------------------
        print("=== TEST 1: Step 1 High Beams Active (t = 0.8s) ===")
        page.click("button[data-step='1']")
        page.wait_for_timeout(300)

        hud_box = page.locator("#telemetry-hud-card").bounding_box()
        ego_tag_box = page.locator("#tag-veh-ego").bounding_box()
        pill_box = page.locator("#hud-status-pill").bounding_box()

        overlap_hud_ego = check_overlap(hud_box, ego_tag_box)
        overlap_pill_hud = check_overlap(pill_box, hud_box)
        print(f"Step 1 Overlaps: HUD/Ego: {overlap_hud_ego}, Pill/HUD: {overlap_pill_hud}")
        assert not overlap_hud_ego, "HUD overlaps Ego tag in Step 1!"
        assert not overlap_pill_hud, "Status pill overlaps HUD in Step 1!"

        page.screenshot(path=os.path.join(output_dir, 'step1_high_beams_active.png'))

        # -------------------------------------------------------------
        # TEST 2: Step 2 Oncoming Vehicle Detected (t = 2.8s)
        # -------------------------------------------------------------
        print("=== TEST 2: Step 2 Oncoming Traffic Detected (t = 2.8s) ===")
        page.click("button[data-step='2']")
        page.wait_for_timeout(300)

        ego_tag_box = page.locator("#tag-veh-ego").bounding_box()
        onc_tag_box = page.locator("#tag-veh-oncoming").bounding_box()
        hud_box = page.locator("#telemetry-hud-card").bounding_box()

        overlap_ego_onc = check_overlap(ego_tag_box, onc_tag_box)
        overlap_hud_ego = check_overlap(hud_box, ego_tag_box)
        overlap_hud_onc = check_overlap(hud_box, onc_tag_box)
        print(f"Step 2 Overlaps: Ego/Onc: {overlap_ego_onc}, HUD/Ego: {overlap_hud_ego}, HUD/Onc: {overlap_hud_onc}")
        assert not overlap_ego_onc, "Ego tag overlaps Oncoming tag in Step 2!"
        assert not overlap_hud_ego, "HUD overlaps Ego tag in Step 2!"
        assert not overlap_hud_onc, "HUD overlaps Oncoming tag in Step 2!"

        page.screenshot(path=os.path.join(output_dir, 'step2_oncoming_detected.png'))

        # -------------------------------------------------------------
        # TEST 3: Step 3 500-FT Mandatory Dimming Point (t = 4.8s)
        # -------------------------------------------------------------
        print("=== TEST 3: Step 3 500-FT Mandatory Dimming Point (t = 4.8s) ===")
        page.click("button[data-step='3']")
        page.wait_for_timeout(300)

        ego_tag_box = page.locator("#tag-veh-ego").bounding_box()
        onc_tag_box = page.locator("#tag-veh-oncoming").bounding_box()
        hud_box = page.locator("#telemetry-hud-card").bounding_box()

        overlap_ego_onc = check_overlap(ego_tag_box, onc_tag_box)
        overlap_hud_ego = check_overlap(hud_box, ego_tag_box)
        print(f"Step 3 Overlaps: Ego/Onc: {overlap_ego_onc}, HUD/Ego: {overlap_hud_ego}")
        assert not overlap_ego_onc, "Ego tag overlaps Oncoming tag in Step 3!"
        assert not overlap_hud_ego, "HUD overlaps Ego tag in Step 3!"

        # Verify beam mode in DOM
        beam_mode_text = page.locator("#telem-beam-mode").inner_text()
        assert "LOW BEAMS" in beam_mode_text, f"Expected Low Beams in Step 3, got: {beam_mode_text}"

        page.screenshot(path=os.path.join(output_dir, 'step3_500ft_dimming_mandate.png'))

        # -------------------------------------------------------------
        # TEST 4: Step 4 Safe Glare-Free Passing (t = 6.8s)
        # -------------------------------------------------------------
        print("=== TEST 4: Step 4 Safe Glare-Free Passing (t = 6.8s) ===")
        page.click("button[data-step='4']")
        page.wait_for_timeout(300)

        ego_tag_box = page.locator("#tag-veh-ego").bounding_box()
        comp_box = page.locator("#compliance-badge").bounding_box()
        overlap_comp_ego = check_overlap(comp_box, ego_tag_box)
        print(f"Step 4 Overlaps: Comp/Ego: {overlap_comp_ego}")
        assert not overlap_comp_ego, "Compliance badge overlaps Ego tag in Step 4!"

        page.screenshot(path=os.path.join(output_dir, 'step4_safe_passing_restored.png'))

        # -------------------------------------------------------------
        # TEST 5: Mode 2 Following Traffic 300 FT Dimming Rule (t = 3.8s)
        # -------------------------------------------------------------
        print("=== TEST 5: Mode 2 Following Traffic 300 FT Dimming Rule (t = 3.8s) ===")
        page.click("#mode-btn-2")
        page.wait_for_timeout(300)
        page.evaluate("timelineSlider.value = 3.8; updateSimulation(3.8);")
        page.wait_for_timeout(300)

        ego_tag_box = page.locator("#tag-veh-ego").bounding_box()
        lead_tag_box = page.locator("#tag-veh-lead").bounding_box()
        hud_box = page.locator("#telemetry-hud-card").bounding_box()

        overlap_ego_lead = check_overlap(ego_tag_box, lead_tag_box)
        overlap_hud_ego = check_overlap(hud_box, ego_tag_box)
        overlap_hud_lead = check_overlap(hud_box, lead_tag_box)
        print(f"Mode 2 Overlaps: Ego/Lead: {overlap_ego_lead}, HUD/Ego: {overlap_hud_ego}, HUD/Lead: {overlap_hud_lead}")
        assert not overlap_ego_lead, "Ego tag overlaps Lead tag in Mode 2!"
        assert not overlap_hud_ego, "HUD overlaps Ego tag in Mode 2!"
        assert not overlap_hud_lead, "HUD overlaps Lead tag in Mode 2!"

        page.screenshot(path=os.path.join(output_dir, 'mode2_following_300ft_dimming.png'))

        # -------------------------------------------------------------
        # TEST 6: Mode 3 Critical Hazard Demo (Glare & Drift, t = 4.8s)
        # -------------------------------------------------------------
        print("=== TEST 6: Mode 3 Hazard Demo Glare & Drift (t = 4.8s) ===")
        page.click("#mode-btn-3")
        page.wait_for_timeout(300)
        page.evaluate("timelineSlider.value = 4.8; updateSimulation(4.8);")
        page.wait_for_timeout(300)

        banner_box = page.locator("#hazard-banner").bounding_box()
        hud_box = page.locator("#telemetry-hud-card").bounding_box()
        pill_box = page.locator("#hud-status-pill").bounding_box()

        overlap_banner_hud = check_overlap(banner_box, hud_box)
        overlap_banner_pill = check_overlap(banner_box, pill_box)
        print(f"Mode 3 Overlaps: Banner/HUD: {overlap_banner_hud}, Banner/Pill: {overlap_banner_pill}")
        assert not overlap_banner_hud, "Hazard banner overlaps HUD in Mode 3!"
        assert not overlap_banner_pill, "Hazard banner overlaps status pill in Mode 3!"

        page.screenshot(path=os.path.join(output_dir, 'mode3_hazard_glare_centerline_drift.png'))

        browser.close()

    print("\n=== CONSOLE LOGS & ERRORS ===")
    print(f"Total Console Logs: {len(console_logs)}")
    for l in console_logs:
        print(f"   {l}")
    print(f"Total JS Errors: {len(js_errors)}")
    for err in js_errors:
        print(f"   ERROR: {err}")

    assert len(js_errors) == 0, f"Found {len(js_errors)} JavaScript errors!"
    print("Lesson 18 verification and capture complete!")

if __name__ == '__main__':
    test_l05_t10()
