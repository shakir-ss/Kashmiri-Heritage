Feature: Customer Inquiries
    As a customer of The Hundred Villages platform
    I want to contact the support team with my queries
    So that I can get assistance with products or orders

    @ui @smoke @positive
    Scenario: Submit a contact inquiry and verify in admin dashboard
        Given I am on the Contact page
        When I fill in the contact form with:
            | field   | value                         |
            | name    | Test User                     |
            | email   | test@example.com              |
            | phone   | 9906000000                    |
            | subject | Order Support                 |
            | message | I need help with my pashmina. |
        And I click the "Send Message" button
        Then I should see "Message Received"
        And I should see "Thank you for reaching out"
        
        # Verify in Admin Dashboard
        Given I am logged in as admin on the UI
        And I am on the Admin Dashboard
        Then I should see the "Customer Inquiries" section
        And I should see an inquiry from "Test User" with subject "Order Support"
