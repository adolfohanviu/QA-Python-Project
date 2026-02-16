import os
import logging
from pathlib import Path
from typing import Generator
import pytest
from playwright.async_api import async_playwright, Browser, BrowserContext, Page

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def headless() -> bool:
    """Get headless mode from env or default to True"""
    headless_env = os.getenv("HEADLESS", "true").lower()
    return headless_env != "false"


@pytest.fixture(scope="session")
def browser_type():
    """Get browser type from env or default to chromium"""
    return os.getenv("BROWSER_TYPE", "chromium")


@pytest.fixture(scope="session")
async def browser(headless, browser_type) -> Generator[Browser, None, None]:
    """Create browser instance"""
    async with async_playwright() as p:
        if browser_type == "firefox":
            browser = await p.firefox.launch(headless=headless)
        elif browser_type == "webkit":
            browser = await p.webkit.launch(headless=headless)
        else:  # chromium
            browser = await p.chromium.launch(headless=headless)
        
        yield browser
        await browser.close()


@pytest.fixture
async def context(browser) -> Generator[BrowserContext, None, None]:
    """Create browser context"""
    context = await browser.new_context()
    yield context
    await context.close()


@pytest.fixture
async def page(context) -> Generator[Page, None, None]:
    """Create page instance"""
    page = await context.new_page()
    yield page
    
    # Take screenshot on failure
    if not getattr(page, "_test_passed", True):
        screenshot_dir = Path("tests/screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        screenshot_path = screenshot_dir / f"failure_{page._test_name}.png"
        await page.screenshot(path=str(screenshot_path))
        logger.info(f"Screenshot captured: {screenshot_path}")
    
    await page.close()


@pytest.fixture(autouse=True)
def test_context():
    """Store test metadata"""
    class TestContext:
        passed = True
        name = ""
    
    yield TestContext()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture test result"""
    outcome = yield
    if outcome.excinfo is not None:
        item._test_passed = False
