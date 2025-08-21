from playwright.sync_api import sync_playwright

def before_all(context):
    playwright = sync_playwright().start()
    context.browser = playwright.chromium.launch(headless=False)
    context.page = context.browser.new_page()

def after_scenario(context, scenario):
    if scenario.status == "failed":
        context.page.screenshot(path=f"screenshots/{scenario.name}.png")

def after_all(context):
    context.browser.close()