Feature: Inventory and Stock Management
    As a customer or admin of the Kashmiri Dry Fruits platform
    I want stock levels to be accurately tracked and reflected
    So that I don't order items that are unavailable

    @ui @regression @stock
    Scenario: Product shows out of stock after all items are purchased
        Given I am logged in as admin on the UI
        And a category exists with ID 1
        And I create a product with name "Limited Edition Box", price 5000, stock 2, and details "Only 2 available"
        And I am on the Products page
        Then I should see product "Limited Edition Box"
        And product "Limited Edition Box" should show "2 available" or "In Stock"
        
        When I click on product "Limited Edition Box"
        And I add 2 items to the cart
        And I go to the Cart page
        And I click the modal button "Proceed to Checkout"
        And I fill in address "Test Address" and phone "1234567890"
        And I click the modal button "Pay & Place Order"
        Then I should see "Order Placed Successfully!"
        
        When I go to the Products page
        Then product "Limited Edition Box" should show "Out of Stock"
        And the "Add to Cart" button for "Limited Edition Box" should be disabled
