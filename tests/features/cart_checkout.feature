Feature: Cart and Checkout
    As a customer of the Kashmiri Dry Fruits platform
    I want to manage my cart and place orders

    @api @smoke @positive
    Scenario: Add item to cart via API
        Given I am logged in as admin via API
        And a product exists with ID 1
        When I add 2 units of product 1 to the cart
        Then the cart should contain 2 units of product 1
        And the status code should be 200

    @api @regression @negative
    Scenario: Add non-existent product to cart via API
        Given I am logged in as admin via API
        When I add 1 unit of product 999 to the cart
        Then the status code should be 404

    @api @smoke @positive
    Scenario: Place an order via API
        Given I am logged in as admin via API
        And my cart contains items
        When I place an order with address "123 Walnut St" and phone "9876543210"
        Then the order should be created successfully
        And the cart should be cleared
        And the status code should be 201

    @ui @smoke @positive
    Scenario: Complete full checkout flow via UI
        Given I am logged in as admin on the UI
        And I am on the Home page
        When I add "Mamra Almonds" to the cart
        And I go to the Cart page
        And I click the "Proceed to Checkout" button
        And I fill in address "Kashmir, Srinagar" and phone "+91 9988776655"
        And I click the "Pay & Place Order" button
        Then I should see "Order Placed Successfully!"
        And I should see my order in the order history

    @ui @regression
    Scenario: Navigate to product detail from cart
        Given I am on the Home page
        When I add "Mamra Almonds" to the cart
        And I go to the Cart page
        When I click on the product icon for "Mamra Almonds"
        Then I should be on the detail page for "Mamra Almonds"
