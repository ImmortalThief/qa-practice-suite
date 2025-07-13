from playwright.sync_api import sync_playwright
from datetime import datetime
import os

def save_screenshot(page, label="manual_test"):
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/{label}_{timestamp}.png"
        os.makedirs("screenshots", exist_ok=True)
        page.screenshot(path=filename)
        print(f"📸 Screenshot saved: {filename}")
    except Exception as e:
        print(f"⚠️ Screenshot failed: {e}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Set to True if you don't want to see the browser
    page = browser.new_page()
    page.goto("https://www.saucedemo.com/")       # Open any page you'd like
    save_screenshot(page, label="manual_test")    # Try saving screenshot manually
    browser.close()
