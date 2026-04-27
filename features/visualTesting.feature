@Regression
Feature: Visual Testing Feature

  @VisualTesting
  Scenario: Visual Testing
    Given I navigate to Selenium Website
    When I capture the actual image
    Then I verify the image should match with the baseline