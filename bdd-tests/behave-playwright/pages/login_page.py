from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = "#user-name"
        self.password_input = "#password"
        self.login_button = "#login-button"
        self.error_message = "h3[data-test='error']"

    def open(self):
        self.page.goto("https://www.saucedemo.com/")

    def login(self, username: str, password: str):
        self.page.fill(self.username_input, username)
        self.page.fill(self.password_input, password)
        self.page.click(self.login_button)

    def login_without_credentials(self):
        self.page.click(self.login_button)

    def get_error_message(self):
        return self.page.inner_text(self.error_message)
    
    def error_message_visible(self):
        return self.page.is_visible(self.error_message)