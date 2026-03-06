import pytest
import logging
from tests.pageobjects.login_page import LoginPage
from tests.utils.config import config

# pytest class setup assigns fixture-backed attributes intentionally.
# pylint: disable=attribute-defined-outside-init

logger = logging.getLogger(__name__)


@pytest.mark.ui
class TestLoginFlow:
    """UI tests for login functionality"""
    
    @pytest.fixture(autouse=True)
    async def setup(self, page):
        """Setup test - navigate to login page"""
        self.page = page
        self.login_page = LoginPage(page)
        await self.login_page.goto(config.base_url)
    
    @pytest.mark.smoke
    async def test_successful_login(self):
        """Test successful login with valid credentials"""
        await self.login_page.login("standard_user", "secret_sauce")
        # Verify inventory page is loaded
        assert await self.login_page.is_visible(".inventory_list"), \
            "Inventory list should be visible after successful login"
        logger.info("✓ Login test passed")
    
    @pytest.mark.regression
    async def test_invalid_password_login(self):
        """Test login with invalid password - should show error message"""
        await self.login_page.login("standard_user", "wrong_password")
        # Verify error message is displayed
        assert await self.login_page.is_visible(LoginPage.ERROR_MESSAGE), \
            "Error message should be visible for invalid password"
        error_text = await self.login_page.get_error_message()
        assert "Epic sadface" in error_text or "password" in error_text.lower(), \
            f"Expected password error message, got: {error_text}"
        logger.info("✓ Invalid password test passed")
