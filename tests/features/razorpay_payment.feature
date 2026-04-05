Feature: Payment Integration & Checkout Robustness
  As a customer of The Hundred Villages platform
  I want to pay for my order securely
  So that my acquisition is confirmed and artisanal products are reserved

  @ui @regression @smoke @mock
  Scenario: Rapid End-to-End Checkout using QA Mock Bypass
    Given I am logged in as admin on the UI
    And I am on the Products page
    When I add "Wild Himalayan White Honey" to the cart
    And I go to the Cart page
    And I click the button "Proceed to Checkout"
    And I fill in "Full Name" with "QA Regression Tester"
    And I fill in "Phone Number" with "9906000000"
    And I fill in "Shipping Address" with "Test Suite Lane"
    And I fill in "City" with "Srinagar"
    And I fill in "Area Pincode" with "190001"
    And I select payment mode "QA Mock Payment"
    And I agree to the terms
    And I click the button "Authorize Full Payment"
    Then I should see "Order Secured Successfully!"
    And I should see "Complete Your Acquisition"
    And my order status should be "paid" in the database

  @ui @payments @razorpay @netbanking @provider-verify
  Scenario: Complete a successful Razorpay payment using Netbanking
    Given I am logged in as admin on the UI
    And I am on the Home page
    When I add "Wild Himalayan White Honey" to the cart
    And I go to the Cart page
    And I click the button "Proceed to Checkout"
    And I fill in "Full Name" with "Netbanking Tester"
    And I fill in "Phone Number" with "9906000001"
    And I fill in "Shipping Address" with "Gulmarg Meadows"
    And I fill in "City" with "Gulmarg"
    And I fill in "Area Pincode" with "193403"
    And I select payment mode "Instant Confirmation (UPI)"
    And I agree to the terms
    And I click the button "Authorize Full Payment"
    Then I should see the Razorpay checkout modal
    When I complete the Razorpay payment with Netbanking
    And I click "Success" on the bank gateway
    Then I should see "Order Secured Successfully!"
    And I should see "Complete Your Acquisition"
    And my order status should be "paid" in the database
