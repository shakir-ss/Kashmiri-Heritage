Feature: Cart and Checkout
    As a customer of The Hundred Villages platform
    I want to manage my cart and place orders

    @api @smoke @positive
    Scenario: Add item to cart via API
        Given I am logged in as admin via API
        And a product exists with ID 1
        When I add 2 units of product 1 to the cart
        Then the cart should contain 2 units of product 1
        And the status code should be 201

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

    @ui @smoke @positive @shipping
    Scenario: Complete checkout with local pincode free delivery
        Given I am logged in as admin on the UI
        And I am on the Home page
        When I add "Premium Mamra Almonds" to the cart
        And I go to the Cart page
        And I click the modal button "Proceed to Checkout"
        And I fill in "Full Name" with "Local Customer"
        And I fill in "Phone Number" with "+91 9988776655"
        And I fill in "Shipping Address" with "Srinagar Downtown"
        And I fill in "City" with "Srinagar"
        And I fill in "Area Pincode" with "190001"
        Then I should see "COMPLIMENTARY" in delivery charges
        When I agree to the terms
        And I click the modal button "Authorize Full Payment"
        Then I should see "Order Secured Successfully!"


    @ui @regression @payments
    Scenario: Verify Partial COD commitment messaging and breakdown
        Given I am logged in as admin on the UI
        And I am on the Home page
        When I add "Premium Mamra Almonds" to the cart
        And I go to the Cart page
        And I click the modal button "Proceed to Checkout"
        And I fill in "City" with "Delhi"
        And I fill in "Area Pincode" with "110001"
        When I select payment mode "Partial COD (Trust & Commitment)"
        Then I should see "Due Today (30%)"
        And I should see "Pay on Arrival (70%)"
        And I should see "Smart Choice!"

    @ui @regression @compliance
    Scenario: Verify terms agreement is mandatory for checkout
        Given I am logged in as admin on the UI
        And I am on the Home page
        When I add "Premium Mamra Almonds" to the cart
        And I go to the Cart page
        And I click the modal button "Proceed to Checkout"
        When I click the modal button "Authorize Full Payment"
        Then I should see "Please agree to terms"


    @ui @regression
    Scenario: Navigate to product detail from cart
        Given I am on the Home page
        When I add "Premium Mamra Almonds" to the cart
        And I go to the Cart page
        When I click on the product icon for "Premium Mamra Almonds"
        Then I should be on the detail page for "Premium Mamra Almonds"
