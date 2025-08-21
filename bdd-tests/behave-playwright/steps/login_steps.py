from behave import given, when, then
from pages.login_page import LoginPage

@given("I am on the login page")
def step_open_login_page(context):
    context.login_page = LoginPage(context.page)
    context.login_page.open()

@when('I login with username "{username}" and password "{password}"')
def step_login_with_credentials(context, username, password):
    context.login_page.login(username, password)

@when("I attempt to login without entering any credentials")
def step_login_blank(context):
    context.login_page.login_without_credentials()

@then('I should be redirected to the inventory page')
def step_inventory_redirect(context):
    assert "inventory" in context.page.url, f"❌ Expected inventory page, got {context.page.url}"

@then('I should see the heading "Products"')
def step_inventory_heading(context):
    heading = context.page.inner_text(".title")
    assert heading == "Products", f"❌ Expected heading 'Products', got {heading}"

@then('I should see an error message containing "{expected_text}"')
def step_error_message(context, expected_text):
    actual = context.login_page.get_error_message()
    assert expected_text in actual, f"❌ Expected '{expected_text}', got '{actual}'"

@when("I reload the page")
def step_reload(context):
    context.page.reload()

@then("the error message should not be visible")
def step_error_not_visible(context):
    assert not context.login_page.error_message_visible(), "❌ Error message still visible after reload"