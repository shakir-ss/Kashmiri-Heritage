Feature: Wishlist Management
    As a customer of the Kashmiri Heritage platform
    I want to save my favorite products to a wishlist
    So that I can purchase them later

    @api @smoke @positive
    Scenario: Add item to wishlist via API
        Given I register and login as a regular user
        And a product exists with ID 1
        When I add product 1 to my wishlist
        Then the API should return a success message "Added to wishlist"
        And the status code should be 201

    @ui @smoke @positive
    Scenario: Toggle wishlist on product card
        Given I am logged in as admin on the UI
        And I am on the Products page
        When I click the wishlist icon on product "Premium Mamra Almonds"
        Then the wishlist icon for "Premium Mamra Almonds" should be active
        And I should see 1 item in my wishlist count

    @ui @regression @positive
    Scenario: View and manage items in Wishlist page
        Given I am logged in as admin on the UI
        And I have "Premium Mamra Almonds" in my wishlist
        When I go to the Wishlist page
        Then I should see "Premium Mamra Almonds" in the wishlist grid
        When I click "Remove" for "Premium Mamra Almonds"
        Then I should see "Your wishlist is empty"
