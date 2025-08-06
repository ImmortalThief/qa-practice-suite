import os
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError

# Utility function to save a screenshot with a timestamped filename
def save_screenshot(page, label="inventory"):
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

# Main test function to validate the "inventory_page_navigation" scenario
def test_inventory_page_navigation():
    # Start Playwright manually to retain control of browser shutdown
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False) # Use headless=True if running in CI
    context = browser.new_context()
    page = context.new_page()

    try:
        print("🔗 Navigating to login page...")
        page.goto("https://www.saucedemo.com/")

        print("Filling in credentials...")
        page.fill("input#user-name", "standard_user")
        page.fill("input#password", "secret_sauce")
        page.click("input#login-button")

        print("Waiting for dashboard...")
        page.wait_for_url("**/inventory.html", timeout=5000)

        assert page.url.startswith("https://www.saucedemo.com/inventory.html")
        print("✅ Login successful! Test passed.")

        heading_text = page.inner_text(".title") # The "Products" heading has class 'title'
        assert heading_text.strip() == "Products", f"❌ Expected 'Products' but got '{heading_text}'" # Using .strip() to avoid whitespace issues
        print("✅ 'Products' heading is visible")

        item_count = page.locator(".inventory_item").count()
        assert item_count == 6, f"❌ Expected 6 items, but found {item_count}"
        print(f"✅ {item_count} items on page")
    
    except (TimeoutError, AssertionError) as e:
        # Catch expected issues: incorrect navigation or incorrect number of items on page
        print(f"❌ Test failed: {e}")
        save_screenshot(page, label="inventory_page_navigation_failure")

    except Exception as e:
        # Catch anything else: Playwright crash, bad selectors, etc.
        print(f"❌ Unexpected error: {e}")
        save_screenshot(page, label="inventory_unexpected_error")

    finally:
        # Close browser and stop Playwright safely
        browser.close()
        p.stop()

# Entry point: Run the test if the script is executed directly
if __name__ == "__main__":
    test_inventory_page_navigation()