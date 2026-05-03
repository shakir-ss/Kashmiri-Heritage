Feature: Role-Based Access Control (3-Tier Permissions)
    As the platform owner
    I want sub-admins to have restricted permissions
    So that only root admins can perform destructive or financial operations

    @api @smoke @positive @rbac
    Scenario: Admin can delete a product via API
        Given I am logged in as admin via API
        And a test product "Delete Test Product" exists
        When I delete the test product via API
        Then the status code should be 200

    @api @smoke @negative @rbac
    Scenario: Sub-admin cannot delete a product via API
        Given I am logged in as sub-admin via API
        And a product exists with ID 1
        When I try to delete product 1 via API
        Then the status code should be 403
        And the API should return an error message containing "Root admin"

    @api @regression @negative @rbac
    Scenario: Sub-admin cannot modify product price via API
        Given I am logged in as sub-admin via API
        And a product exists with ID 1
        When I try to update the price of product 1 to 9999 via API
        Then the status code should be 403

    @api @smoke @negative @rbac
    Scenario: Regular customer cannot access admin order list
        Given I register and login as a regular user
        When I request the admin order list
        Then the status code should be 403

    @ui @regression @rbac
    Scenario: Sub-admin does not see delete buttons on admin dashboard
        Given I am logged in as sub-admin on the UI
        And I am on the Admin Dashboard
        Then I should not see any "Delete" buttons on the Products table
        And I should not see the Revenue analytics cards

    @ui @regression @rbac
    Scenario: Admin sees all controls including delete buttons
        Given I am logged in as admin on the UI
        And I am on the Admin Dashboard
        Then I should see "Delete" buttons on the Products table
        And I should see the Revenue analytics cards
