Feature: Admin Order Management
    As an administrator of the Kashmiri Heritage platform
    I want to see all customer orders and their details
    So that I can fulfill them and monitor shop performance

    @api @smoke @positive
    Scenario: Admin fetches all orders via API
        Given I am logged in as admin via API
        When I request the admin order list
        Then the API should return a list of all customer orders
        And the status code should be 200

    @api @regression @negative
    Scenario: Regular customer cannot fetch admin order list
        Given I register and login as a regular user
        When I request the admin order list
        Then the status code should be 403

    @ui @smoke @positive
    Scenario: Admin views orders on the Dashboard
        Given I am logged in as admin on the UI
        And I am on the Admin Dashboard
        Then I should see the "Recent Customer Orders" table
        And the table should contain at least one order
