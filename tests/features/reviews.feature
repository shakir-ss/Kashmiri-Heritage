Feature: Product Reviews and Cross-sell
    As a customer of The Hundred Villages platform
    I want to read and write product reviews
    And discover related products
    So that I can make informed purchasing decisions

    # ========= REVIEWS =========

    @api @smoke @positive @reviews
    Scenario: Logged-in user submits a product review via API
        Given I am logged in as admin via API
        And a product exists with ID 1
        When I submit a review for product 1 with rating 5 and comment "Excellent quality, highly recommend!"
        Then the API should return a success message "Review added successfully"
        And the status code should be 201

    @api @smoke @positive @reviews
    Scenario: Product detail API includes reviews list
        Given the API is accessible
        When I request product details for product 1
        Then the response should contain a "reviews" field
        And the status code should be 200

    @api @regression @negative @reviews
    Scenario: Guest user cannot submit a review
        Given the API is accessible
        When I submit a review for product 1 with rating 4 and comment "Good" without authentication
        Then the status code should be 401

    @api @regression @negative @reviews
    Scenario: Review with invalid rating is rejected
        Given I am logged in as admin via API
        When I submit a review for product 1 with rating 6 and comment "Invalid"
        Then the status code should be 400
        And the API should return an error message containing "rating"

    @ui @smoke @positive @reviews
    Scenario: Logged-in customer sees review form on product detail page
        Given I am logged in as admin on the UI
        And I am on the Products page
        When I click on product "Premium Mamra Almonds"
        Then I should see the product detail page for "Premium Mamra Almonds"
        And I should see the Customer Reviews section
        And I should see "Write a Review" form with rating selector

    @ui @regression @positive @reviews
    Scenario: Customer submits a review and it appears immediately
        Given I am logged in as admin on the UI
        And I am on the Products page
        When I click on product "Premium Mamra Almonds"
        And I scroll to the "Customer Reviews" section
        And I select rating 5 in the review form
        And I enter review comment "Top quality product from the Valley"
        And I click "Submit Review"
        Then I should see "Top quality product from the Valley" in the reviews list

    # ========= CROSS-SELL =========

    @ui @regression @positive @cross-sell
    Scenario: Related products section appears on product detail page
        Given I am on the Products page
        When I click on product "Premium Mamra Almonds"
        Then I should see the product detail page for "Premium Mamra Almonds"
        And I should see the You May Also Love section
        And I should see at least 1 related product card

    @ui @regression @positive @cross-sell
    Scenario: Clicking a related product navigates to its detail page
        Given I am on the Products page
        When I click on product "Premium Mamra Almonds"
        And I click on the first related product in "You May Also Love"
        Then I should be on a product detail page
