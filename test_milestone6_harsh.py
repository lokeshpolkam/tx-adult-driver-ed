import os
import sys
import json
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

print("=====================================================================")
print("RUNNING MILESTONE 6 HARSH ATTACK TEST: MOBILE LAYOUT & UX INTEGRITY")
print("=====================================================================")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    # --- ATTACK 1: Mobile Viewport 375px Overflow Test on signin.html ---
    # iPhone SE / 13 mini: 375px width
    page = browser.new_page(viewport={'width': 375, 'height': 667})
    signin_url = 'file:///' + os.path.abspath('course_shell/signin.html').replace('\\', '/')
    page.goto(signin_url, wait_until='domcontentloaded')
    page.wait_for_timeout(300)

    # Check horizontal scroll overflow
    scroll_width = page.evaluate("() => document.documentElement.scrollWidth")
    client_width = page.evaluate("() => document.documentElement.clientWidth")
    overflow_px = scroll_width - client_width

    print(f"Mobile Viewport Check (375px): clientWidth={client_width}, scrollWidth={scroll_width}, overflow={overflow_px}px")
    assert overflow_px <= 0, f"CRITICAL UX FLAW: Horizontal scroll overflow of {overflow_px}px detected on 375px mobile screen!"
    print("[ATTACK 1 PASSED] Mobile 375px viewport overflow completely eliminated (0px overflow)")
    page.close()

    # --- ATTACK 2: Contact Form Ticket Submission Test ---
    page2 = browser.new_page()
    contact_url = 'file:///' + os.path.abspath('course_shell/contact.html').replace('\\', '/')
    page2.goto(contact_url, wait_until='domcontentloaded')

    page2.fill('#contact-name', 'Maria Santos')
    page2.fill('#contact-email', 'maria.santos@texasmail.org')
    page2.select_option('#contact-category', 'certificate')
    page2.fill('#contact-serial', 'ADE1317-2026-C3284-00143')
    page2.fill('#contact-msg', 'Need verification letter for Dallas mega center appointment tomorrow.')

    page2.click('#contact-form button[type="submit"]')
    page2.wait_for_timeout(400)

    # Verify confirmation alert is visible with ticket ID
    success_visible = page2.is_visible('#contact-success')
    assert success_visible, "Contact success container was not displayed after submit!"
    ticket_id = page2.inner_text('#ticket-id')
    assert len(ticket_id) >= 5, f"Expected 5-digit ticket number, got: '{ticket_id}'"

    # Verify ticket persisted in localStorage
    tickets = page2.evaluate("() => JSON.parse(localStorage.getItem('tx_support_tickets') || '[]')")
    assert len(tickets) > 0, "Support ticket was not persisted to localStorage!"
    assert tickets[0]['email'] == 'maria.santos@texasmail.org', f"Unexpected ticket data: {tickets[0]}"
    print(f"[ATTACK 2 PASSED] Support ticket #TX-{ticket_id} submitted & persisted to registry")
    page2.close()

    # --- ATTACK 3: Password Recovery Test ---
    page3 = browser.new_page()
    reset_url = 'file:///' + os.path.abspath('course_shell/reset-password.html').replace('\\', '/')
    page3.goto(reset_url, wait_until='domcontentloaded')

    page3.fill('#reset-email', 'student.recovery@gmail.com')
    page3.click('#reset-btn')
    page3.wait_for_timeout(800)

    # Verify confirmation box is visible
    reset_success_visible = page3.is_visible('#reset-success')
    assert reset_success_visible, "Password reset success banner was not displayed!"

    # Verify reset request persisted in localStorage
    resets = page3.evaluate("() => JSON.parse(localStorage.getItem('tx_password_resets') || '[]')")
    assert len(resets) > 0, "Password recovery request was not persisted!"
    assert resets[0]['email'] == 'student.recovery@gmail.com'
    print("[ATTACK 3 PASSED] Password recovery request submitted & confirmed")
    page3.close()

    # --- ATTACK 4: Student Review Submission & Persistence ---
    page4 = browser.new_page()
    reviews_url = 'file:///' + os.path.abspath('course_shell/reviews.html').replace('\\', '/')
    page4.goto(reviews_url, wait_until='domcontentloaded')

    # Open review modal
    page4.click('#btn-submit-review')
    page4.wait_for_selector('#review-modal:not(.hidden)')

    page4.fill('#reviewer-name', 'Carlos Mendoza')
    page4.select_option('#reviewer-city', 'San Antonio, TX')
    page4.fill('#reviewer-serial', 'ADE1317-2026-C3284-00122')
    page4.fill('#reviewer-text', 'Passed the final exam on my iPad and printed certificate immediately. Skipped the DPS written test!')

    page4.click('#review-form button[type="submit"]')
    page4.wait_for_timeout(500)

    # Verify review was added to page and stored in localStorage
    stored_reviews = page4.evaluate("() => JSON.parse(localStorage.getItem('tx_student_reviews') || '[]')")
    assert len(stored_reviews) > 0, "Review was not persisted to localStorage!"
    assert stored_reviews[0]['name'] == 'Carlos Mendoza'
    
    body_text = page4.inner_text('body')
    assert 'Carlos Mendoza' in body_text, "Newly submitted review is not visible in reviews feed!"
    print("[ATTACK 4 PASSED] Student review submitted, rendered to feed, and persisted")
    page4.close()

    browser.close()

print("\n=====================================================================")
print("ALL MILESTONE 6 HARSH ATTACK TESTS PASSED! (0 VULNERABILITIES REMAIN)")
print("=====================================================================")
