Feature: Product Discovery - Faceted Filters, Predictive Search & Mega Menu
    As a customer of The Hundred Villages platform
    I want to filter, search, and discover products efficiently
    So that I can find the right product quickly

    # ========= FACETED FILTERS =========

    @api @smoke @positive @filters
    Scenario: Filter products by minimum price via API
        Given the API is accessible
        When I request products with min_price 500
        Then all returned products should have price greater than or equal to 500
        And the status code should be 200

    @api @smoke @positive @filters
    Scenario: Filter products by price range via API
        Given the API is accessible
        When I request products with min_price 100 and max_price 1000
        Then all returned products should have price between 100 and 1000
        And the status code should be 200

    @api @smoke @positive @search
    Scenario: Fuzzy search products via API using "q" parameter
        Given the API is accessible
        When I search for products with keyword "almond" using the "q" parameter
        Then the API should return products matching "almond"
        And the status code should be 200

    @api @regression @positive @search
    Scenario: Search by product description keyword via API
        Given the API is accessible
        When I search for products with keyword "Pampore" using the "q" parameter
        Then the API should return products whose description contains "Pampore"
        And the status code should be 200

    @ui @smoke @positive @filters
    Scenario: Price filter narrows product grid on Products page
        Given I am on the Products page
        When I enter min price 500 and max price 2000 in the price filter
        Then the product grid should update
        And all visible products should be within the price range 500 to 2000

    @ui @regression @positive @search
    Scenario: Search bar filters products in real time
        Given I am on the Products page
        When I type "walnut" in the search bar
        Then the product grid should show only products matching "walnut"

    # ========= MEGA MENU =========

    @ui @smoke @positive @mega-menu
    Scenario: Mega menu opens on hover over Products link
        Given I am on the Home page
        When I hover over the "Products" navigation link
        Then I should see the mega menu dropdown
        And I should see product category cards in the mega menu

    @ui @regression @positive @mega-menu
    Scenario: Category card in mega menu navigates to filtered products
        Given I am on the Home page
        When I hover over the "Products" navigation link
        And I click on a category card in the mega menu
        Then I should be on the Products page
        And the category filter should be applied

    @ui @regression @positive @mega-menu
    Scenario: Predictive search in mega menu returns results
        Given I am on the Home page
        When I hover over the "Products" navigation link
        And I type "saffron" in the mega menu search box
        Then I should see product suggestions in the mega menu dropdown
