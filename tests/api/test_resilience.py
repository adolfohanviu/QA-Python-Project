"""Fault-injection tests for APIClient's retry/timeout behavior.

Runs against the WireMock mock (mocks/mappings/), not the live jsonplaceholder
API - jsonplaceholder can't be made to fail on demand, so there's no other way
to exercise these paths for real. Start the mock first:
    docker compose --profile mock up -d wiremock
or a standalone WireMock jar with --root-dir mocks. Skips cleanly if the mock
isn't reachable.
"""
import os

import pytest
import requests

from tests.api.api_client import APIClient

WIREMOCK_BASE_URL = os.getenv("WIREMOCK_BASE_URL", "http://localhost:8081")


@pytest.mark.resilience
class TestAPIClientResilience:
    """APIClient retry/timeout behavior under fault injection."""

    @pytest.fixture
    def mock_client(self) -> APIClient:
        """APIClient pointed at WireMock, with scenario state reset first."""
        try:
            response = requests.post(f"{WIREMOCK_BASE_URL}/__admin/scenarios/reset", timeout=2)
            response.raise_for_status()
        except requests.exceptions.RequestException as exc:
            pytest.skip(
                f"WireMock not reachable at {WIREMOCK_BASE_URL} ({exc}) - "
                "start it with `docker compose --profile mock up -d wiremock`."
            )
        return APIClient(base_url=WIREMOCK_BASE_URL)

    def test_get_retries_through_transient_failures_then_succeeds(self, mock_client: APIClient):
        """/flaky-users fails twice (503) then recovers - client should retry and succeed."""
        response = mock_client.get("/flaky-users")

        assert response.status_code == 200
        assert mock_client.get_json()[0]["name"] == "Automation User"

    def test_get_retries_through_a_connection_drop_then_succeeds(self, mock_client: APIClient):
        """/dropped-users resets the connection once then recovers - client should retry."""
        response = mock_client.get("/dropped-users")

        assert response.status_code == 200

    def test_get_gives_up_after_max_retries_on_persistent_failure(self, mock_client: APIClient):
        """/broken-users always fails - client should exhaust retries and surface the 503."""
        response = mock_client.get("/broken-users")

        assert response.status_code == 503

    def test_get_times_out_instead_of_hanging_on_a_slow_response(self, mock_client: APIClient):
        """/slow-users delays 3s; a 1s client timeout must raise, not hang for 3s."""
        mock_client.timeout = 1
        mock_client.max_retries = 0

        with pytest.raises(requests.exceptions.Timeout):
            mock_client.get("/slow-users")
