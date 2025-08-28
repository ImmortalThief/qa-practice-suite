# ==============================
# File: login_page.py
# Purpose: Page Object for the SauceDemo login screen
# Encapsulates locators and actions so step definitions
# interact with methods instead of raw selectors.
# ==============================

from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        # Element locators
        self.username_input = "#user-name"
        self.password_input = "#password"
        self.login_button = "#login-button"
        self.error_message = "h3[data-test='error']"

    def open(self):
        # Navigate to the login screen
        self.page.goto("https://www.saucedemo.com/")

    def login(self, username: str, password: str):
        # Fill in user credentials and submit forms
        self.page.fill(self.username_input, username)
        self.page.fill(self.password_input, password)
        self.page.click(self.login_button)

    def login_without_credentials(self):
        # Submit form without entering values (used for validation tests)
        self.page.click(self.login_button)

    def get_error_message(self):
        # Return text of the displayed error banner
        return self.page.inner_text(self.error_message)
    
    def error_message_visible(self):
        # Check whether an error banner is currently visible
        return self.page.is_visible(self.error_message)