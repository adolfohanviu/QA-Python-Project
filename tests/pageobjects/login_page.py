import logging
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from tests.pageobjects.base_page import BasePage

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """Login page object for Sauce Demo application.
    
    Handles login functionality and error state management.
    Inherits common page functionality from BasePage.
    """
    
    # Selectors for login form elements
    USERNAME_INPUT = "[data-test='username']"
    PASSWORD_INPUT = "[data-test='password']"
    LOGIN_BUTTON = "[data-test='login-button']"
    ERROR_MESSAGE = "[data-test='error']"
    
    async def login(self, username: str, password: str) -> None:
        """Perform login with username and password

        Args:
            username (str): Username to log in with
            password (str): Password to log in with

        Note:
            Waits for navigation to inventory page on success,
            or checks for error message on failure.

        Raises:
            TimeoutError: if login neither navigates to the inventory page
                nor shows an error message within the timeout - an ambiguous
                state (slow-loading form, unexpected page) a caller should
                not have to infer from an unrelated assertion failing later.
        """
        logger.info("Logging in with username: %s", username)
        await self.fill_text(self.USERNAME_INPUT, username)
        await self.fill_text(self.PASSWORD_INPUT, password)
        await self.click(self.LOGIN_BUTTON)

        # Wait for navigation or error
        try:
            await self.page.wait_for_url("**/inventory.html", timeout=5000)
            logger.info("Login successful")
            return
        except PlaywrightTimeoutError as exc:
            logger.debug("Navigation timeout during login: %s", type(exc).__name__)

        # Check for error message
        if await self.is_visible(self.ERROR_MESSAGE):
            error = await self.get_text(self.ERROR_MESSAGE)
            logger.error("Login failed: %s", error)
            return

        raise TimeoutError(
            f"Login for user '{username}' neither navigated to the inventory page "
            "nor showed an error message within the timeout."
        )
    
    async def get_error_message(self) -> str:
        """Get error message text from login form
        
        Returns:
            str: Error message text
            
        Raises:
            PlaywrightError: If error message not found
        """
        return await self.get_text(self.ERROR_MESSAGE)
