import os
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError

# Helper funtion to save a screenshot with a timestamped filename
def save_screenshot(page, label="failure"):
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/{label}_{timestamp}.png"

        # Ensure screenshots directory exists
        os.makedirs("screenshots", exist_ok=True)

        # Capture screenshot of current page
        page.screenshot(path=filename)
        print(f"📸 Screenshot saved: {filename}")
    except Exception as e:
        print(f"⚠️ Screenshot failed: {e}")

# Main test function for invalid login scenario
def test_invalid_login():
    # Launch Playwright and Chromium browser
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False) # Use headless=True for CI/CD later
    context = browser.new_context()
    page = context.new_page()

    try:
        print("🔗 Navigating to login page...")
        page.goto("http://www.saucedemo.com/")

        print("🔐 Entering invalid credentials...")
        page.fill("input#user-name", "standard_user") # Correct username
        page.fill("input#password", "wrong_password") # Incorrect password
        page.click("input#login-button")

        # Assert that the login does NOT succeed by checking the URL
        # If it *does* succeed, that's a failure for this test
        # assert page.url != "https://www.saucedemo.com/inventory.html", "❌ Unexpected login success"
        # Force a failure to verify screenshot works
        assert page.url == "https://www.saucedemo.com/inventory.html", "❌ Forcing failure to test screenshot"

        print("✅ Login correctly failed. Test passed.")

    # Handle expected assertion failure (login was incorrectly accepted)
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
        save_screenshot(page, label="invalid_login")

    # Catch anything else unexpected (timeouts, selector errors, etc.)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        save_screenshot(page, label="unexpected_error")

    finally:
        browser.close()
        p.stop()

# Entry point for the script
if __name__ == "__main__":
    test_invalid_login()