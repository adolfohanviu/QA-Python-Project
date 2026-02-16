import pytest
import logging
from tests.api.api_client import APIClient
from tests.utils.config import config

logger = logging.getLogger(__name__)


@pytest.mark.api
class TestUserAPI:
    """API tests for user endpoints"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup API client"""
        self.client = APIClient()
    
    @pytest.mark.smoke
    def test_get_all_users(self):
        """Test GET /users endpoint"""
        response = self.client.get("/users")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        logger.info(f"Retrieved {len(data)} users")
    
    @pytest.mark.regression
    def test_get_user_by_id(self):
        """Test GET /users/1 endpoint"""
        response = self.client.get("/users/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert "name" in data
        assert "email" in data
    
    @pytest.mark.regression
    def test_create_user_with_fixture(self):
        """Test POST /users with fixture data"""
        fixture_data = config.load_fixture("userBasic")
        response = self.client.post("/users", fixture_data)
        assert response.status_code in [200, 201]
        data = response.json()
        assert data["name"] == fixture_data["name"]
        assert data["email"] == fixture_data["email"]
    
    @pytest.mark.regression
    def test_update_user_with_fixture(self):
        """Test PUT /users/1 with fixture data"""
        fixture_data = config.load_fixture("userUpdate")
        response = self.client.put("/users/1", fixture_data)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == fixture_data["email"]
    
    @pytest.mark.regression
    def test_delete_user(self):
        """Test DELETE /users/1 endpoint"""
        response = self.client.delete("/users/1")
        assert response.status_code == 200
