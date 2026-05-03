Feature: 1-Click Reorder and B2B Wholesale Inquiry
    As a customer of The Hundred Villages platform
    I want to reorder past purchases and submit wholesale inquiries
    So that I can shop efficiently and explore business partnerships

    # ========= 1-CLICK REORDER =========

    @api @smoke @positive @reorder
    Scenario: User order history contains product_id for reorder
        Given I am logged in as admin via API
        When I fetch my order history via API
        Then each order item should contain a "product_id" field

    @ui @regression @positive @reorder
    Scenario: Buy Again button adds items back to cart
        Given I am logged in as admin on the UI
        And I have at least one past order
        When I navigate to the orders page
        And I click "Buy Again" for the first past order
        Then I should be redirected to the cart page
        And the cart should contain items from the past order

    # ========= B2B WHOLESALE PORTAL =========

    @ui @smoke @positive @b2b
    Scenario: Wholesale portal page is accessible from navbar
        Given I am on the Home page
        When I click the "Wholesale" link in the navigation
        Then I should be on the Wholesale page
        And I should see "Wholesale Partnership" on the page

    @api @smoke @positive @b2b
    Scenario: Submit a B2B wholesale inquiry via API
        When I submit a B2B inquiry with company "Valley Traders", email "traders@example.com", phone "9876543210", and requirements "500kg walnuts per month"
        Then the API should return a success message "B2B inquiry submitted successfully"
        And the status code should be 201

    @ui @regression @positive @b2b
    Scenario: Submit wholesale inquiry via the UI form
        Given I am on the Wholesale page
        When I fill in the wholesale form with company "Kashmir Exports", email "exports@test.com", phone "9988776600", and requirements "Bulk saffron and almonds for export"
        And I click "Submit Inquiry" on the wholesale form
        Then I should see "Thank you" or "submitted" on the page

    @api @regression @negative @b2b
    Scenario: B2B inquiry with missing required fields is rejected
        When I submit a B2B inquiry with company "", email "bad@test.com", phone "9876543210", and requirements ""
        Then the status code should be 400
