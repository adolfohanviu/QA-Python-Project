Feature: User API contract validation
  As a QA engineer
  I want to validate user API behavior with BDD scenarios
  So that contract-level API behavior is readable and executable

  @api @contract @smoke @bdd
  Scenario: Retrieve all users successfully
    Given the API client is available
    When I request all users
    Then the response status should be 200
    And the response should contain a non-empty user list

  @api @contract @regression @bdd
  Scenario: Create user with fixture payload
    Given the API client is available
    When I create a user using fixture "userBasic"
    Then the response status should be 201
    And the response should include fixture field "name"
    And the response should include fixture field "email"
