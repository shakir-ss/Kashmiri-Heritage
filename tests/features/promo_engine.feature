Feature: Promo Code Engine
    As a customer of The Hundred Villages platform
    I want to apply promotional discount codes at checkout
    So that I can get discounts on my orders

    Background:
        Given I am logged in as admin via API

    @api @smoke @positive @promo
    Scenario: Apply a valid promo code via API
        Given a promo code "HERITAGE20" exists with 20 percent discount
        And my cart contains items
        When I apply promo code "HERITAGE20" via API
        Then the API should return a discount percentage of 20
        And the status code should be 200

    @api @regression @negative @promo
    Scenario: Apply an invalid or expired promo code via API
        Given my cart contains items
        When I apply promo code "FAKECODE99" via API
        Then the status code should be 404
        And the API should return an error message containing "not found"

    @ui @smoke @positive @promo
    Scenario: Apply promo code HERITAGE20 at checkout and verify discount
        Given I am logged in as admin on the UI
        And I am on the Home page
        When I add "Premium Mamra Almonds" to the cart
        And I go to the Cart page
        And I click the modal button "Proceed to Checkout"
        And I fill in "Full Name" with "Promo Customer"
        And I fill in "Phone Number" with "9988776655"
        And I fill in "Shipping Address" with "Test Lane"
        And I fill in "City" with "Srinagar"
        And I fill in "Area Pincode" with "190001"
        When I enter promo code "HERITAGE20" and click Apply
        Then I should see a discount applied in the order summary
        And I should see "HERITAGE20" confirmed on the page

    @api @regression @negative @promo
    Scenario: Apply a promo code exceeding max uses
        Given a promo code "MAXED99" exists with 0 remaining uses
        And my cart contains items
        When I apply promo code "MAXED99" via API
        Then the status code should be 400
        And the API should return an error message containing "maximum uses"
