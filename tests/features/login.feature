Feature: Login flow
  As a user
  I want to authenticate with valid credentials
  So that I can access the inventory page

  @ui @smoke @bdd
  Scenario: Successful login with valid credentials
    Given I am on the login page
    When I log in with username "standard_user" and password "secret_sauce"
    Then I should see the inventory page
