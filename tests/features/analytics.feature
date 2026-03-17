Feature: Analytics
    As an admin of the Kashmiri Heritage platform
    I want to track product views and see shop stats

    @api @smoke @positive
    Scenario: Track product view via API
        Given the API is accessible
        When I view product with ID 1
        Then the status code should be 200

    @api @smoke @positive
    Scenario: Admin can fetch stats via API
        Given I am logged in as admin via API
        When I fetch the shop stats
        Then the API should return a stats object
        And the status code should be 200

    @api @regression @negative
    Scenario: Regular user cannot fetch stats via API
        Given I register and login as a regular user
        When I fetch the shop stats
        Then the status code should be 403
