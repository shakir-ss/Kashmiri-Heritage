Feature: Admin Inventory Management
    As an administrator of The Hundred Villages platform
    I want to manage the product inventory efficiently
    So that I can keep the catalog up to date

    @ui @admin @inventory @positive
    Scenario: Admin toggles product visibility using active status
      Given I am logged in as admin on the UI
      And I am on the Admin Dashboard
      When I click on "Edit" for product "Hand-Embroidered Sozni Pashmina"
      And I uncheck the "Show on Website (Active)" checkbox
      And I click the modal button "Save Product"
      Then the status for "Hand-Embroidered Sozni Pashmina" should be "Inactive"
      When I go to the Products page
      Then I should not see product "Hand-Embroidered Sozni Pashmina"
      When I am on the Admin Dashboard
      And I click on "Edit" for product "Hand-Embroidered Sozni Pashmina"
      And I check the "Show on Website (Active)" checkbox
      And I click the modal button "Save Product"
      Then the status for "Hand-Embroidered Sozni Pashmina" should be "Active"
      When I go to the Products page
      Then I should see product "Hand-Embroidered Sozni Pashmina"

