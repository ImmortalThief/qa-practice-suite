# ==============================
# File: login_steps.py
# Purpose: Step definitions for login.feature
# Behave decorators (@given, @when, @then) connect natural language
# steps from the .feature file to executable Python code.
# ==============================

from behave import given, when, then
from pages.login_page import LoginPage

@given("I am on the login page")
def step_open_login_page(context):                  
    context.login_page = LoginPage(context.page)    # Create a LoginPage object and navigate to the login screen
    context.login_page.open()                       

@when('I login with username "{username}" and password "{password}"')   
def step_login_with_credentials(context, username, password):           
    context.login_page.login(username, password)        # Credentials are injected from the feature file placeholders                       

@when("I attempt to login without entering any credentials")    
def step_login_blank(context):                                  
    context.login_page.login_without_credentials()      # Negative path: trigger validation by submitting an empty form

@then('I should be redirected to the inventory page')                                               
def step_inventory_redirect(context):                                                               
    assert "inventory" in context.page.url, f"❌ Expected inventory page, got {context.page.url}"   # URL check ensures we actually navigated away from login   

@then('I should see the heading "Products"')
def step_inventory_heading(context):
    heading = context.page.inner_text(".title")     # '.title' is a static selector for the Swag Labs inventory header
    assert heading == "Products", f"❌ Expected heading 'Products', got {heading}"

@then('I should see an error message containing "{expected_text}"')     
def step_error_message(context, expected_text):                         
    actual = context.login_page.get_error_message()     # Error messages vary depending on the cause (blank, locked out, etc.)
    assert expected_text in actual, f"❌ Expected '{expected_text}', got '{actual}'"

@when("I reload the page")
def step_reload(context):
    context.page.reload()       # Reload resets page state(useful for clearing temporary UI elements)

@then("the error message should not be visible")                                                            
def step_error_not_visible(context):                                                                        
    assert not context.login_page.error_message_visible(), "❌ Error message still visible after reload"    # Ensures validation messages don't persist across reloads