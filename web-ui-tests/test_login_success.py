from playwright.sync_api import sync_playwright, TimeoutError

def test_login_success():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            print("Opening login page...")
            page.goto("https://www.saucedemo.com/")

            print("Filling in credentials...")
            page.fill("input#user-name","standard_user")
            page.fill("input#password","secret_sauce")
            page.click("input#login-button")

            print("Waiting for dashboard...")
            page.wait_for_url("**/inventory.html", timeout=5000)

            assert page.url == "https://www.saucedemo.com/inventory.html"
            print("✅ Login successful! Test passed.")

            browser.close()
    except TimeoutError:
        print("❌ ERROR: Timed out waiting for login to complete.")
    except AssertionError:
        print("❌ ERROR: URL assertion failed. Login may not have worked.")
    except Exception as e:
        print(f"❌ ERROR: Unexpected exception: {e}")
    
if __name__ =="__main__":
    test_login_success()