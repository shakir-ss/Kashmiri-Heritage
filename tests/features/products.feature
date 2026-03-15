Feature: Product Management
    As a user or admin of the Kashmiri Dry Fruits platform
    I want to browse, search, and manage products

    @api @smoke @positive
    Scenario: Fetch all categories via API
        Given the API is accessible
        When I request categories from the API
        Then the API should return a list of categories
        And the status code should be 200

    @api @smoke @positive
    Scenario: Search for products by name via API
        Given the API is accessible
        When I search for products with keyword "Mamra"
        Then the API should return products matching "Mamra"
        And the status code should be 200

    @api @smoke @positive
    Scenario: Create a new product as admin with full details via API
        Given I am logged in as admin via API
        And a category exists with ID 1
        When I create a product with name "Saffron Honey", price 800, stock 30, and details "Pure honey infused with Pampore saffron"
        Then the API should return a success message "Product created successfully"
        And the status code should be 201

    @api @regression @positive
    Scenario: Create product without image via API
        Given I am logged in as admin via API
        And a category exists with ID 1
        When I create a product with name "No Image Item", price 100, stock 10, and no image URL
        Then the API should return a success message "Product created successfully"
        And the status code should be 201

    @api @regression @negative
    Scenario: Create product without authorization via API
        Given the API is accessible
        When I try to create a product without an auth token
        Then the API should return an error message "Token is missing!"
        And the status code should be 401

    @ui @smoke @positive
    Scenario: Browse product list via UI
        Given I am on the Products page
        Then I should see a list of products
        And I should see product "Premium Mamra Almonds"

    @ui @smoke @positive
    Scenario: View product detail page
        Given I am on the Products page
        When I click on product "Premium Mamra Almonds"
        Then I should see the product detail page for "Premium Mamra Almonds"
        And I should see the product story "Our Mamra Almonds are sourced"

    @ui @regression @positive
    Scenario: Admin adds product with multiple images and detailed story
        Given I am logged in as admin on the UI
        And I am on the Admin Dashboard
        When I fill in the product form with name "Kashmiri Kahwa Set", price 1500, stock 10, and details "Authentic copper samovar with 6 cups"
        And I add an additional image URL "https://via.placeholder.com/600x800?text=Kahwa+1"
        And I add an additional image URL "https://via.placeholder.com/600x800?text=Kahwa+2"
        And I click the "Save Product" button
        Then I should see the product "Kashmiri Kahwa Set" in the product list
        When I am on the Products page
        And I click on product "Kashmiri Kahwa Set"
        Then I should see the product detail page for "Kashmiri Kahwa Set"
        And I should see 3 images in the gallery

    @ui @admin @categories
    Scenario: Admin manages categories via Dashboard
        Given I am logged in as admin on the UI
        And I am on the Admin Dashboard
        When I click "+ New Category"
        And I fill in category name "Handicrafts" and description "Exquisite Kashmiri art"
        And I click the modal button "Save Category"
        Then I should see the category "Handicrafts" in the category list
        When I edit the category "Handicrafts" to name "Art & Crafts"
        And I click the modal button "Save Category"
        Then I should see the category "Art & Crafts" in the category list
