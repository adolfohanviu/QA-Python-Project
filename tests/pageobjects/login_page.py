import logging
from playwright.async_api import Page
from tests.pageobjects.base_page import BasePage

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """Login page object"""
    
    USERNAME_INPUT = "[data-test='username']"
    PASSWORD_INPUT = "[data-test='password']"
    LOGIN_BUTTON = "[data-test='login-button']"
    ERROR_MESSAGE = "[data-test='error']"
    
    async def login(self, username: str, password: str):
        """Perform login"""
        logger.info(f"Logging in with username: {username}")
        await self.fill_text(self.USERNAME_INPUT, username)
        await self.fill_text(self.PASSWORD_INPUT, password)
        await self.click(self.LOGIN_BUTTON)
        
        # Wait for navigation or error
        try:
            await self.page.wait_for_url("**/inventory.html", timeout=5000)
            logger.info("Login successful")
        except:
            # Check for error message
            if await self.is_visible(self.ERROR_MESSAGE):
                error = await self.get_text(self.ERROR_MESSAGE)
                logger.error(f"Login failed: {error}")
    
    async def get_error_message(self) -> str:
        """Get error message text"""
        return await self.get_text(self.ERROR_MESSAGE)
