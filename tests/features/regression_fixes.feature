Feature: Regression & UAT Improvements
  As a QA Engineer
  I want to verify that recent cart and UI improvements are working correctly
  To ensure a premium and bug-free e-commerce experience

  Background:
    Given I am logged in as admin on the UI

  @ui @cart @uat
  Scenario: Verify Save to Wishlist from Cart
    Given I am on the Products page
    When I add "Premium Mamra Almonds" to the cart
    And I go to the Cart page
    And I click "Save to Wishlist" for "Premium Mamra Almonds"
    Then "Premium Mamra Almonds" should be removed from the cart
    And "Premium Mamra Almonds" should be in my wishlist

  @ui @cart @inventory
  Scenario: Verify Out of Stock handling in Cart
    Given I am on the Products page
    When I add "Organic Saffron" to the cart
    And "Organic Saffron" becomes out of stock
    And I go to the Cart page
    Then I should see the status "⚠️ Currently Out of Stock" for item "Organic Saffron"
    And the quantity controls for "Organic Saffron" should be disabled
    And the item total for "Organic Saffron" should be "Unavailable"
    And the Cart Total should not include "Organic Saffron"

  @ui @navigation @breadcrumbs
  Scenario: Verify Heritage Breadcrumbs on Product Detail
    Given I am on the Products page
    When I click on product icon for "Hand-Embroidered Sozni Pashmina"
    Then I should see the breadcrumb path "Home > Heritage Catalog > Hand-Embroidered Sozni Pashmina"

  @ui @mobile @uat
  Scenario: Verify Sticky Mobile Action Bar on Product Detail
    Given I am using a mobile device with width 375
    And I am on the Products page
    When I click on product icon for "Premium Mamra Almonds"
    And I scroll down 800 pixels
    Then I should see the sticky mobile action bar
    And it should show the price and "Add to Cart" button

  @ui @support
  Scenario: Verify Floating Artisan Support Button
    Given I am on the Home page
    Then I should see the floating support button
    And it should show "Talk to an Artisan" when hovered
