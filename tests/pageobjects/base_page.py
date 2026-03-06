import logging
from playwright.async_api import Page

logger = logging.getLogger(__name__)


class BasePage:
    """Base page object with common functionality for all pages.
    
    Provides standard methods for navigation, element interaction,
    and assertions that can be reused across all page objects.
    """
    
    def __init__(self, page: Page):
        """Initialize page object
        
        Args:
            page (Page): Playwright page instance
        """
        self.page = page
    
    async def goto(self, url: str, timeout: int = 30000):
        """Navigate to URL with timeout
        
        Args:
            url (str): URL to navigate to
            timeout (int): Navigation timeout in milliseconds (default: 30000)
            
        Raises:
            PlaywrightError: If navigation fails or times out
        """
        logger.info("Navigating to %s", url)
        await self.page.goto(url, timeout=timeout)
    
    async def fill_text(self, selector: str, text: str):
        """Fill text input field
        
        Args:
            selector (str): CSS selector of the input element
            text (str): Text to fill in
            
        Raises:
            PlaywrightError: If element not found or not fillable
        """
        logger.info("Filling %s with text", selector)
        await self.page.fill(selector, text)
    
    async def click(self, selector: str):
        """Click on element
        
        Args:
            selector (str): CSS selector of the element
            
        Raises:
            PlaywrightError: If element not found or not clickable
        """
        logger.info("Clicking %s", selector)
        await self.page.click(selector)
    
    async def is_visible(self, selector: str) -> bool:
        """Check if element is visible
        
        Args:
            selector (str): CSS selector of the element
            
        Returns:
            bool: True if element is visible, False otherwise
        """
        return await self.page.is_visible(selector)
    
    async def get_text(self, selector: str) -> str:
        """Get element text content
        
        Args:
            selector (str): CSS selector of the element
            
        Returns:
            str: Text content of the element
            
        Raises:
            PlaywrightError: If element not found
        """
        text = await self.page.text_content(selector)
        logger.debug("Retrieved text from %s: %s", selector, text)
        return text
    
    async def take_screenshot(self, name: str):
        """Take screenshot and save to file
        
        Args:
            name (str): Name of the screenshot (without extension)
            
        Raises:
            PlaywrightError: If screenshot capture fails
        """
        await self.page.screenshot(path=f"tests/screenshots/{name}.png")
        logger.info("Screenshot taken: %s", name)

