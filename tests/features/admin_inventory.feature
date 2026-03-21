Feature: Admin Inventory Management
    As an administrator of The Hundred Villages platform
    I want to manage the product inventory efficiently
    So that I can keep the catalog up to date

    @ui @smoke @positive
    Scenario: Navigate to product detail from Admin Dashboard inventory list
        Given I am logged in as admin on the UI
        And I am on the Admin Dashboard
        When I click on the product name "Premium Mamra Almonds" in the inventory table
        Then I should be on the detail page for "Premium Mamra Almonds"
