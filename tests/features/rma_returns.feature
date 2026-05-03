Feature: Self-Service RMA (Returns)
    As a customer of The Hundred Villages platform
    I want to request a return for a delivered order
    So that I can get a refund or replacement

    @api @smoke @positive @rma
    Scenario: Submit a return request for a delivered order via API
        Given I am logged in as admin via API
        And I have a delivered order
        When I submit a return request for the order with reason "Product damaged in transit"
        Then the API should return a success message "Return requested successfully"
        And the status code should be 201

    @api @regression @negative @rma
    Scenario: Submit a return request for a non-delivered order via API
        Given I am logged in as admin via API
        And I have a pending order
        When I submit a return request for the order with reason "Changed my mind"
        Then the status code should be 400
        And the API should return an error message containing "only for delivered orders"

    @ui @regression @rma
    Scenario: Customer sees Request Return button for delivered orders
        Given I am logged in as admin on the UI
        And I have a delivered order visible in order history
        When I navigate to the orders page
        Then I should see a "Request Return" button for the delivered order

    @ui @regression @rma
    Scenario: Customer submits return request via modal
        Given I am logged in as admin on the UI
        And I have a delivered order visible in order history
        When I navigate to the orders page
        And I click "Request Return" for the delivered order
        And I enter return reason "Product quality not as described" in the modal
        And I click "Submit Return Request" in the modal
        Then I should see "Return request submitted" on the page
