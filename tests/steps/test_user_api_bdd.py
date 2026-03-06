import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from tests.api.api_client import APIClient
from tests.utils.config import config

pytestmark = [pytest.mark.api, pytest.mark.contract, pytest.mark.bdd]

scenarios("../features/user_api.feature")


@pytest.fixture(name="scenario_ctx")
def scenario_context() -> dict:
    return {}


@given("the API client is available")
def given_api_client(scenario_ctx: dict):
    scenario_ctx["client"] = APIClient()


@when("I request all users")
def when_request_all_users(scenario_ctx: dict):
    scenario_ctx["response"] = scenario_ctx["client"].get("/users")


@when(parsers.parse('I create a user using fixture "{fixture_name}"'))
def when_create_user_with_fixture(scenario_ctx: dict, fixture_name: str):
    scenario_ctx["payload"] = config.load_fixture(fixture_name)
    scenario_ctx["response"] = scenario_ctx["client"].post("/users", scenario_ctx["payload"])


@then(parsers.parse("the response status should be {status_code:d}"))
def then_validate_status_code(scenario_ctx: dict, status_code: int):
    assert scenario_ctx["response"].status_code == status_code, (
        f"Expected {status_code}, got {scenario_ctx['response'].status_code}"
    )


@then("the response should contain a non-empty user list")
def then_validate_non_empty_user_list(scenario_ctx: dict):
    body = scenario_ctx["response"].json()
    assert isinstance(body, list), "Response body should be a list"
    assert len(body) > 0, "Response should include at least one user"


@then(parsers.parse('the response should include fixture field "{field_name}"'))
def then_validate_response_matches_fixture(scenario_ctx: dict, field_name: str):
    body = scenario_ctx["response"].json()
    expected = scenario_ctx["payload"][field_name]
    assert body[field_name] == expected, (
        f"Expected field '{field_name}' to be '{expected}', got '{body[field_name]}'"
    )
