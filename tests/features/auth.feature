Feature: User Authentication
    As a user of the The Hundred Villages platform
    I want to be able to register and log in
    So that I can access my account and place orders

    @api @smoke
    Scenario: Register a new user via API
        Given the API is accessible
        When I register a new user with name "Test User", email "newuser@example.com", and password "password123"
        Then the API should return a success message "Registered successfully"
        And the status code should be 201

    @api @smoke
    Scenario: Login with valid credentials via API
        Given I have a registered user with email "root@thehundredvillages.com" and password "root123"
        When I login via API with email "root@thehundredvillages.com" and password "root123"
        Then the API should return a JWT token
        And the status code should be 200

    @ui @smoke
    Scenario: Login with valid credentials via UI
        Given I am on the Login page
        When I enter email "root@thehundredvillages.com" and password "root123"
        And I click the login button
        Then I should be redirected to the Home page
        And I should see a logout option
