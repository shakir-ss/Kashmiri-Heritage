Feature: Missing Requirements and Improvements

  Scenario: Admin can set an image for a category
    Given I am logged in as an "admin"
    And I submit a POST request to "/api/products/categories" with
      """
      {
        "name": "Luxury Spices",
        "description": "Premium quality",
        "image_url": "https://example.com/spices.jpg"
      }
      """
    Then the response status code should be 201
    And the latest category "Luxury Spices" should have image_url "https://example.com/spices.jpg"

  Scenario: User submits a B2B inquiry and Admin manages it
    Given I am an unauthenticated user
    When I submit a POST request to "/api/orders/b2b/inquiry" with
      """
      {
        "company_name": "Taj Hotels",
        "contact_name": "Ravi",
        "email": "ravi@taj.com",
        "phone": "9999999999",
        "requirements": "100kg Saffron"
      }
      """
    Then the response status code should be 201
    
    Given I am logged in as an "admin"
    When I send a GET request to "/api/orders/b2b/admin"
    Then the response status code should be 200
    And the JSON response should contain an item with "company_name" equal to "Taj Hotels"

  Scenario: Admin adds tracking info and User tracks it
    Given I am logged in as a "customer"
    And I add a product to my cart
    And I submit a POST request to "/api/orders/place" with payment mode "mock"
    And the response status code should be 201
    And I mock verify the payment for the placed order
    Then my order is created and status is "paid"

    Given I am logged in as an "admin"
    When I submit a PUT request to update the order status to "shipped" with tracking link "https://track.com/123"
    Then the response status code should be 200

    Given I am an unauthenticated user
    When I track my order using the order ID and my email
    Then the response status code should be 200
    And the JSON response should have "tracking_link" equal to "https://track.com/123"

  Scenario: Abandoned Cart capture triggers automatically
    Given I am an unauthenticated user
    When I submit an abandoned cart payload with email "lost@cart.com"
    Then the response status code should be 200
    And the abandoned cart for "lost@cart.com" should exist in the database

  Scenario: User submits a review with an image
    Given I am logged in as a "customer"
    When I submit a POST request to "/api/reviews/" for product 1 with image "http://image.com/1.jpg"
    Then the response status code should be 201
    And the product 1 should have a review containing image "http://image.com/1.jpg"
