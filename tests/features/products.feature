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
    Scenario: Create a new product as admin via API
        Given I am logged in as admin via API
        And a category exists with ID 1
        When I create a product with name "Walnut Kernels", price 1500, and stock 50
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
        And I should see product "Mamra Almonds"

    @ui @regression @positive
    Scenario: Admin adds product via Dashboard
        Given I am logged in as admin on the UI
        And I am on the Admin Dashboard
        When I fill in the product form with name "Saffron 1g", price 450, stock 20, and category ID 1
        And I click the "Save Product" button
        Then I should see the product "Saffron 1g" in the product list
