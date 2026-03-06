import pytest
import logging
from tests.api.api_client import APIClient
from tests.utils.config import config

logger = logging.getLogger(__name__)


@pytest.mark.api
@pytest.mark.contract
class TestUserAPI:
    """API tests for user endpoints"""

    @pytest.fixture
    def client(self) -> APIClient:
        """Provide API client per test for isolation."""
        return APIClient()
    
    @pytest.mark.smoke
    def test_get_all_users(self, client: APIClient):
        """Test GET /users endpoint - retrieves all users"""
        response = client.get("/users")
        assert response.status_code == 200, \
            f"Expected 200, got {response.status_code}"
        data = response.json()
        assert isinstance(data, list), "Response should be a list"
        assert len(data) > 0, "Should return at least one user"
        logger.info("Retrieved %s users", len(data))
    
    @pytest.mark.regression
    def test_get_user_by_id(self, client: APIClient):
        """Test GET /users/1 endpoint - retrieves specific user"""
        response = client.get("/users/1")
        assert response.status_code == 200, \
            f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["id"] == 1, "User ID should match request"
        assert "name" in data, "User should have 'name' field"
        assert "email" in data, "User should have 'email' field"
        logger.info("Retrieved user: %s", data.get("name"))
    
    @pytest.mark.regression
    def test_create_user_with_fixture(self, client: APIClient):
        """Test POST /users with fixture data"""
        fixture_data = config.load_fixture("userBasic")
        response = client.post("/users", fixture_data)
        assert response.status_code in [200, 201], \
            f"Expected 200/201, got {response.status_code}"
        data = response.json()
        assert data["name"] == fixture_data["name"], "Name should match fixture"
        assert data["email"] == fixture_data["email"], "Email should match fixture"
        logger.info("Created user: %s", data.get("name"))
    
    @pytest.mark.regression
    def test_update_user_with_fixture(self, client: APIClient):
        """Test PUT /users/1 with fixture data"""
        fixture_data = config.load_fixture("userUpdate")
        response = client.put("/users/1", fixture_data)
        assert response.status_code == 200, \
            f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["email"] == fixture_data["email"], "Email should be updated"
        logger.info("Updated user email: %s", data.get("email"))
    
    @pytest.mark.regression
    def test_delete_user(self, client: APIClient):
        """Test DELETE /users/1 endpoint"""
        response = client.delete("/users/1")
        assert response.status_code == 200, \
            f"Expected 200, got {response.status_code}"
        logger.info("User deleted successfully")
