Feature: Login functionality
    As a user of the Swag Labs app
    I want to log in successfully or see clear error messages
    So that I can access the products page

    Scenario: Successful login with valid credentials
        Given I am on the login page
        When I login with username "standard_user" and password "secret_sauce"
        Then I should be redirected to the inventory page
        And I should see the heading "Products"

    Scenario: Login fails with invalid credentials
        Given I am on the login page
        When I login with username "wrong_user" and password "wrong_pass"
        Then I should see an error message containing "Username and password do not match"

    Scenario: Login fails with blank credentials
        Given I am on the login page
        When I attempt to login without entering any credentials
        Then I should see an error message containing "Username is required"

    Scenario: Error message clears on retry
        Given I am on the login page
        When I login with username "wrong_user" and password "wrong_pass"
        Then I should see an error message containing "Username and password do not match"
        When I reload the page
        Then the error message should not be visible