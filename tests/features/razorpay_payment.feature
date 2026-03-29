Feature: Razorpay Payment Integration
  As a customer of The Hundred Villages platform
  I want to pay for my order securely via Razorpay
  So that my acquisition is confirmed and artisanal products are reserved

  @ui @payments @razorpay
  Scenario: Complete a successful Razorpay payment using Test Card
    Given I am logged in as admin on the UI
    And I am on the Home page
    When I add "Premium Mamra Almonds" to the cart
    And I go to the Cart page
    And I click the modal button "Proceed to Checkout"
    And I fill in "Full Name" with "Razorpay Tester"
    And I fill in "Phone Number" with "9906000000"
    And I fill in "Shipping Address" with "Pahalgam Valley"
    And I fill in "City" with "Anantnag"
    And I fill in "Area Pincode" with "192126"
    And I agree to the terms
    And I click the button "Authorize Full Payment"
    Then I should see the Razorpay checkout modal
    When I complete the Razorpay payment with test card "4111111111111111"
    Then I should see "Order Secured Successfully!"
    And my order status should be "paid" in the database
