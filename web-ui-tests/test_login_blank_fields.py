import os
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError

# Utility function to save a screenshot with a timestamped filename
def save_screenshot(page, label="blank_fields"):
    try:
        # Create a filename with a current date and time
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/{label}_{timestamp}.png"

        # Make sure the screenshots directory exists
        os.makedirs("screenshots", exist_ok=True)

        # Take a screenshot of the current page
        page.screenshot(path=filename)
        print(f"📸 Screenshot saved: {filename}")
    except Exception as e:
        # If screenshot fails, log the error (usually means browser is already closed)
        print(f"⚠️ Screenshot failed: {e}")

# Main test function to validate the "blank_fields" login scenario
def test_blank_fields_login():
    # Start Playwright manually to retain control of browser shutdown
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False) # Use headless=True if running in CI
    context = browser.new_context()
    page = context.new_page()

    try:
        print("🔗 Navigating to login page...")
        page.goto("https://www.saucedemo.com/")

        print("😶 Logging in with blank_credentials...")
        page.fill("input#user-name", "") # Blank username
        page.fill("input#password", "") #Blank password
        page.click("input#login-button") #Submit login

        print("🔍 Checking for blank fields error message...")
        error_selector = "h3[data-test='error']"

        # Wait up to 3 seconds for the error message to appear
        page.wait_for_selector(error_selector, timeout=3000)

        # Get the error message text from the page
        error_text = page.inner_text(error_selector)

        # Check if the error mentions blank credentials
        assert "Username is required" in error_text, f"❌ Unexpected error message: {error_text}"

        print("✅ Correct error message displayed. Test passed.")

    except (TimeoutError, AssertionError) as e:
        # Catch expected issues: no message found, or incorrect message
        print(f"❌ Test failed: {e}")
        save_screenshot(page, label="blank_fields_login_failure")

    except Exception as e:
        # Catch anything else: Playwright crash, bad selectors, etc.
        print(f"❌ Unexpected error: {e}")
        save_screenshot(page, label="blank_credentials_unexpected")

    finally:
        # Close browser and stop Playwright safely
        browser.close()
        p.stop()

# Entry point: Run the test if the script is executed directly
if __name__ == "__main__":
    test_blank_fields_login() 