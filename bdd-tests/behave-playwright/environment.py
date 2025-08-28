# ==============================
# File: environment.py
# Purpose: Behave environment hooks for setup/teardown
# Provides browser lifecycle management and logging for test runs.
# ==============================

import logging
from playwright.sync_api import sync_playwright

def before_all(context):
    # Configure run-wide logging (writes to test_summary.log)
    logging.basicConfig(        
        filename="test_summary.log",
        level=logging.INFO,
        FORMAT="%(asctime)s | %(levelname)s | %(message)s"
    )
    logging.info("🚀 Test run started")

    # Start Playwright and open a Chromium browser for the session
    playwright = sync_playwright().start()
    context.browser = playwright.chromium.launch(headless=False)
    context.page = context.browser.new_page()

def before_scenario(context, scenario):
    logging.info(f"▶️ Starting scenario: {scenario.name}")   # Log which scenario begins (Useful for traceability in reports)

def after_scenario(context, scenario):
    if scenario.status == "failed":
        # On failure: capture screenshot + log details for debugging
        screenshot_path = f"screenshots/{scenario.name}.png"
        context.page.screenshot(path=screenshot_path)
        logging.error(f"❌ FAILED: {scenario.name} | URL: {context.page.url} | Screenshot: {screenshot_path}")
    else:
        # On success: simple status log
        logging.info(f"✅ PASSED: {scenario.name}")

def after_all(context):
    # Wrap up: close browser and log end of test run
    logging.info("🏁 Test run finished")
    context.browser.close()