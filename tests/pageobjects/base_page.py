import logging
from playwright.async_api import Page

logger = logging.getLogger(__name__)


class BasePage:
    """Base page object with common functionality"""
    
    def __init__(self, page: Page):
        self.page = page
    
    async def goto(self, url: str):
        """Navigate to URL"""
        logger.info(f"Navigating to {url}")
        await self.page.goto(url)
    
    async def fill_text(self, selector: str, text: str):
        """Fill text input"""
        logger.info(f"Filling {selector} with {text}")
        await self.page.fill(selector, text)
    
    async def click(self, selector: str):
        """Click element"""
        logger.info(f"Clicking {selector}")
        await self.page.click(selector)
    
    async def is_visible(self, selector: str) -> bool:
        """Check if element is visible"""
        return await self.page.is_visible(selector)
    
    async def get_text(self, selector: str) -> str:
        """Get element text"""
        return await self.page.text_content(selector)
    
    async def take_screenshot(self, name: str):
        """Take screenshot"""
        await self.page.screenshot(path=f"tests/screenshots/{name}.png")
        logger.info(f"Screenshot taken: {name}")
