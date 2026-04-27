@Regression
Feature: Registration Feature

  @Login
  Scenario: Login feature - 1
    Given I navigate to Swag Labs
    When I LogIn into the App with personal credentials
    And I verify the user using API
    Then I see Products Page


  @Login
  Scenario: Login feature - 2
    Given I navigate to Swag Labs
    When I LogIn into the App with different credentials
         | UserName       | Password     |
         | visual_user    | secret_sauce |
    Then I see Products Page


  @System
  Scenario Outline: Validating the Registration feature
    Given I navigate to way2automation.com
    When I enter the name as "<name>"
    Then I enter the phone number as "<phonenumber>"
    And I enter the email as "<email>"
    And I enter the country as "<country>"
    And I enter the city as "<city>"
    And I enter the username as "<username>"
    And I enter the password as "<password>"
    And I click on the submit button

    Examples:
      | name         | phonenumber  | email                      | country  | city   | username       | password  |
      | Rahul Arora  | 9711111558   | trainer@way2automation.com | India    | Delhi  | rahularora1985 | ssdfsdfsf |
      | Juan Quiceno | 9711111558   | trainer@way2automation.com | Colombia | Delhi  | rahularora1985 | ssdfsdfsf |


   @System
   Scenario Outline: Validating the Registration feature Negative Path
    Given I navigate to way2automation.com
    When I enter the name as "<name>"
    Then I enter the phone number as "<phonenumber>"
    And I enter the email as "<email>"
    And I enter the country as "<country>"
    And I enter the city as "<city>"
    And I enter the username as "<username>"
    And I enter the password as "<password>"
    And I click on the submit button
    And I see expected Email is "trainer@way2automation.com"

    Examples:
      | name         | phonenumber  | email                      | country  | city   | username       | password  |
      | Rahul Arora  | 9711111558   | trainer@way2automation.com | India    | Delhi  | rahularora1985 | ssdfsdfsf |
      | Juan Quiceno | 9711111558   | trainer@way2automation.com | Colombia | Delhi  | rahularora1985 | ssdfsdfsf |
