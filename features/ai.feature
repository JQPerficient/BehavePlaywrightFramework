@Regression
Feature: AI Feature

  @AI1
  Scenario: Download feature
    Given I navigate to Selenium Download page
    When I ask Gemini for suggested asserts
    """
    Act as an Expert QA Tester
    User opens the Selenium Downloads page.
    User needs the Title of the page and an assert to validate it (share the xpath to find the not title of the page)
    And the user needs the exact xpath to find the title of the page (the xpath to find the visible title of the page)
    And the user validates that the page meets visual presentation standards (share 3 asserts)
    And generate 3 scenarios in guerkin languaje (Given, When, Then) to cover 3 different tests
    """
    Then I download the file


  @AI2
  Scenario: Homepage semantic validation
    Given I navigate to Selenium Homepage
    When I capture the main welcome text
    Then The text should semantically represent a homepage welcome message


  @AI3
  Scenario: Self-healing validation
    Given I navigate to Selenium Homepage
    When I capture the main welcome text
    Then I see expected title


  @MCP @self_healing
  Scenario: Suggest alternative locators when the main hero title locator fails
    Given I navigate to Selenium Homepage
    When I try to capture the main hero title with an invalid locator
    Then Gemini MCP should suggest alternative locators for the element
