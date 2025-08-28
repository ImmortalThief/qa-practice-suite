# NB: The comments are not standard BDD practice. Adding them in since this is my learning repo
# ==============================
# Feature file: login.feature
# Purpose: Defines high-level business scenarios for the login page.
# Written in Gherkin syntax (Given / When / Then).
# These steps link to Python step definitions (login_steps.py).
# ==============================

Feature: Login functionality
    # Business-level description of what we are testing.
    # Goal: Ensure login works correctly, with proper handling of success and failure cases,
    As a user of the Swag Labs app
    I want to log in successfully or see clear error messages
    So that I can access the products page

    # ------------------------------
    # Scenario 1: Positive login flow
    # ------------------------------
    Scenario: Successful login with valid credentials
        Given I am on the login page
        When I login with username "standard_user" and password "secret_sauce"
        Then I should be redirected to the inventory page
        And I should see the heading "Products"

    # ------------------------------
    # Scenario 2: Invalid credentials
    # ------------------------------
    Scenario: Login fails with invalid credentials
        Given I am on the login page
        When I login with username "wrong_user" and password "wrong_pass"
        Then I should see an error message containing "Username and password do not match"

    # ------------------------------
    # Scenario 3: Missing credentials
    # ------------------------------
    Scenario: Login fails with blank credentials
        Given I am on the login page
        When I attempt to login without entering any credentials
        Then I should see an error message containing "Username is required"
        
    # ------------------------------
    # Scenario 4: Error clears on retry
    # ------------------------------
    Scenario: Error message clears on retry
        Given I am on the login page
        When I login with username "wrong_user" and password "wrong_pass"
        Then I should see an error message containing "Username and password do not match"
        When I reload the page
        Then the error message should not be visible