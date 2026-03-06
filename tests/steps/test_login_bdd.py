import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from tests.pageobjects.login_page import LoginPage
from tests.utils.config import config

pytestmark = [pytest.mark.ui, pytest.mark.bdd]

scenarios("../features/login.feature")


@pytest.fixture(name="ui_context")
def login_ui_context() -> dict:
    return {}


@given("I am on the login page")
def given_on_login_page(page, ui_context: dict, event_loop):
    ui_context["login_page"] = LoginPage(page)
    event_loop.run_until_complete(ui_context["login_page"].goto(config.base_url))


@when(parsers.parse('I log in with username "{username}" and password "{password}"'))
def when_login_with_credentials(ui_context: dict, username: str, password: str, event_loop):
    event_loop.run_until_complete(ui_context["login_page"].login(username, password))


@then("I should see the inventory page")
def then_verify_inventory_page_visible(ui_context: dict, event_loop):
    assert event_loop.run_until_complete(ui_context["login_page"].is_visible(".inventory_list")), (
        "Inventory list should be visible after successful login"
    )
