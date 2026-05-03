Feature: Address Book Management
    As a logged-in customer of The Hundred Villages platform
    I want to save and manage my shipping addresses
    So that I can check out faster without re-entering details

    @api @smoke @positive @address-book
    Scenario: Save a shipping address via API
        Given I am logged in as a regular customer via API
        When I save an address with name "Home", line "12 Dal Lake Road", city "Srinagar", state "Jammu & Kashmir", pincode "190001"
        Then the API should return a success message "Address added successfully"
        And the status code should be 201

    @api @smoke @positive @address-book
    Scenario: Fetch saved addresses via API
        Given I am logged in as a regular customer via API
        And I have at least one saved address
        When I fetch my saved addresses via API
        Then the API should return a list of addresses
        And the status code should be 200

    @api @regression @positive @address-book
    Scenario: Delete a saved address via API
        Given I am logged in as a regular customer via API
        And I have at least one saved address
        When I delete my first saved address via API
        Then the status code should be 200

    @api @regression @negative @address-book
    Scenario: Guest user cannot access address book
        Given the API is accessible
        When I request my saved addresses without authentication
        Then the status code should be 401

    @ui @regression @address-book
    Scenario: Address book pre-fills checkout form
        Given I am logged in as admin on the UI
        And I have a saved address "Srinagar Home" in my address book
        When I navigate to the checkout page
        Then I should see the address dropdown with "Srinagar Home"
        When I select "Srinagar Home" from the saved addresses dropdown
        Then the city field should be pre-filled with the saved city
