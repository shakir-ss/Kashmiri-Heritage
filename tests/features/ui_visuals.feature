Feature: UI Visual Validation
    As a user of the Kashmiri Heritage platform
    I want to see all product and category images clearly
    So that I can make informed purchasing decisions

    @ui @smoke @visual
    Scenario: Verify all images on Home Page load correctly
        Given I am on the Home page
        Then all images on the page should be loaded and visible

    @ui @regression @visual
    Scenario: Verify all product images in Catalog load correctly
        Given I am on the Products page
        Then all images on the page should be loaded and visible

    @ui @smoke @visual
    Scenario: Verify hero section background is visible
        Given I am on the Home page
        Then the hero section background should be visible
