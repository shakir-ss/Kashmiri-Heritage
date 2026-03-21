Feature: Inventory and Stock Management
    As a customer or admin of The Hundred Villages platform
    I want stock levels to be accurately tracked and reflected
    So that I don't order items that are unavailable

    @ui @regression @variants
    Scenario: Admin adds product with variants and verifies selection
        Given I am logged in as admin on the UI
        And I am on the Admin Dashboard
        And I click button "+ New Category"
        And I fill in category name "Dry Fruits" and description "Premium Kashmiri nuts"
        And I click the modal button "Save Category"
        And I am on the Admin Dashboard
        When I click the "+ Add New Product" button
        And I fill in "Product Name" with "Multi-Pack Saffron"
        And I fill in "Base Price (₹)" with "500"
        And I select category "Dry Fruits"
        And I fill in "Main Image URL" with "/images/products/saffron.jpg"
        And I fill in "Total Stock" with "50"
        And I click button "+ Add Variant"
        And I fill in variant 1 name "1 gram", modifier 0, and stock 30
        And I click button "+ Add Variant"
        And I fill in variant 2 name "5 grams", modifier 1500, and stock 20
        And I click the modal button "Save Product"
        Then I should see the product "Multi-Pack Saffron" in the product list
        When I am on the Products page
        And I click on product "Multi-Pack Saffron"
        Then I should see the variant chip "1 gram"
        And I should see the variant chip "5 grams"
        When I click variant chip "5 grams"
        Then the price should show "2000"

    @ui @regression @images
    Scenario: Admin adds product with local image path
        Given I am logged in as admin on the UI
        And a category exists with ID 1
        And I am on the Admin Dashboard
        When I fill in the product form with name "Local Image Product", price 100, stock 10, and details "Testing local path"
        And I fill in "Main Image URL" with "/images/products/test-image.jpg"
        And I click the modal button "Save Product"
        Then I should see the product "Local Image Product" in the product list
        When I am on the Products page
        Then product "Local Image Product" should have image source starting with "/images/products/"
