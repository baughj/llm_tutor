#!/usr/bin/env python3
"""
Test script to take screenshots of authentication UI pages using Playwright
"""

from playwright.sync_api import sync_playwright
import time

def test_auth_ui():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 720})
        page = context.new_page()

        # Test Registration Page
        print("📸 Taking screenshot of Registration page...")
        page.goto('http://localhost:3000/register')
        page.wait_for_load_state('networkidle')
        page.screenshot(path='screenshot_register.png')
        print("✓ Registration page screenshot saved")

        # Fill in registration form to show password strength indicator
        print("📸 Taking screenshot of Registration page with form filled...")
        page.fill('input[name="name"]', 'Test User')
        page.fill('input[name="email"]', 'test@example.com')
        page.fill('input[name="password"]', 'MyStr0ng!Pass123')
        page.screenshot(path='screenshot_register_filled.png')
        print("✓ Registration page (filled) screenshot saved")

        # Test Login Page
        print("📸 Taking screenshot of Login page...")
        page.goto('http://localhost:3000/login')
        page.wait_for_load_state('networkidle')
        page.screenshot(path='screenshot_login.png')
        print("✓ Login page screenshot saved")

        # Test Email Verification Page (without token - should show invalid state)
        print("📸 Taking screenshot of Email Verification page...")
        page.goto('http://localhost:3000/verify-email')
        time.sleep(1)  # Wait for state to update
        page.screenshot(path='screenshot_verify_email.png')
        print("✓ Email Verification page screenshot saved")

        # Test responsive design - mobile view
        print("📸 Taking screenshot of Registration page (mobile)...")
        context.set_viewport_size({'width': 375, 'height': 667})
        page.goto('http://localhost:3000/register')
        page.wait_for_load_state('networkidle')
        page.screenshot(path='screenshot_register_mobile.png')
        print("✓ Registration page (mobile) screenshot saved")

        # Close browser
        browser.close()

        print("\n✅ All screenshots taken successfully!")
        print("Screenshots saved:")
        print("  - screenshot_register.png")
        print("  - screenshot_register_filled.png")
        print("  - screenshot_login.png")
        print("  - screenshot_verify_email.png")
        print("  - screenshot_register_mobile.png")

if __name__ == '__main__':
    test_auth_ui()
