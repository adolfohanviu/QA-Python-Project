import os
import logging
from pathlib import Path
from typing import AsyncGenerator

# pytest fixtures and hooks intentionally use injected names/arguments.
# pylint: disable=redefined-outer-name,protected-access,unused-argument

import pytest
import pytest_asyncio
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from tests.utils.observability import (
    configure_observability_file_logging,
    emit_event,
    init_observability,
    new_trace_id,
    observability_enabled,
    reset_trace_id,
    set_trace_id,
    shutdown_observability,
)

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def headless() -> bool:
    """Get headless mode from env or default to True
    
    Returns:
        bool: True if headless mode enabled, False otherwise
    """
    headless_env = os.getenv("HEADLESS", "true").lower()
    return headless_env != "false"


@pytest.fixture(scope="session")
def browser_type() -> str:
    """Get browser type from env or default to chromium
    
    Returns:
        str: Browser type - chromium, firefox, or webkit
    """
    return os.getenv("BROWSER_TYPE", "chromium")


@pytest_asyncio.fixture(scope="function")
async def browser(headless: bool, browser_type: str) -> AsyncGenerator[Browser, None]:
    """Create browser instance for each test function
    
    Args:
        headless: Whether to run in headless mode
        browser_type: Type of browser to launch
        
    Yields:
        Browser: Playwright browser instance
    """
    async with async_playwright() as p:
        if browser_type == "firefox":
            browser = await p.firefox.launch(headless=headless)
        elif browser_type == "webkit":
            browser = await p.webkit.launch(headless=headless)
        else:  # chromium
            browser = await p.chromium.launch(headless=headless)
        
        logger.info("Browser launched: %s (headless=%s)", browser_type, headless)
        yield browser
        await browser.close()
        logger.info("Browser closed: %s", browser_type)


@pytest_asyncio.fixture
async def context(browser: Browser) -> AsyncGenerator[BrowserContext, None]:
    """Create browser context for each test
    
    Args:
        browser: Browser instance from browser fixture
        
    Yields:
        BrowserContext: Isolated browser context
    """
    context = await browser.new_context()
    yield context
    await context.close()


@pytest_asyncio.fixture
async def page(context: BrowserContext, request) -> AsyncGenerator[Page, None]:
    """Create page instance for each test with failure screenshot capture
    
    Args:
        context: Browser context from context fixture
        request: pytest request object for test metadata
        
    Yields:
        Page: Playwright page instance
    """
    page = await context.new_page()
    test_name = request.node.nodeid.replace("::", "_").replace("/", "_").replace("\\", "_")
    
    yield page
    
    # Take screenshot on failure
    try:
        if not getattr(request.node, "_test_passed", True):
            screenshot_dir = Path("tests/screenshots")
            screenshot_dir.mkdir(parents=True, exist_ok=True)
            screenshot_path = screenshot_dir / f"failure_{test_name}.png"
            await page.screenshot(path=str(screenshot_path))
            logger.warning("Test failed. Screenshot captured: %s", screenshot_path)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        logger.error("Failed to capture screenshot: %s", str(exc))
    finally:
        await page.close()


@pytest.fixture(autouse=True)
def test_context():
    """Store test metadata - initializes passed state to True
    
    Yields:
        Object: Test context object to track test state
    """
    class TestContext:
        passed = True
        name = ""
    
    yield TestContext()


@pytest.fixture(autouse=True)
def observability_test_context(request):
    """Create a trace context per test when observability is enabled."""
    if not observability_enabled():
        yield
        return

    trace_id = new_trace_id()
    token = set_trace_id(trace_id)
    emit_event("test_start", test_name=request.node.nodeid)
    try:
        yield
    finally:
        emit_event(
            "test_end",
            test_name=request.node.nodeid,
            passed=getattr(request.node, "_test_passed", True),
        )
        reset_trace_id(token)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture test result - marks failed tests for screenshot capture
    
    Args:
        item: pytest Item object
        call: pytest Call object
    """
    outcome = yield
    if outcome.excinfo is not None:
        item._test_passed = False
        logger.debug("Test failed: %s", item.nodeid)


def pytest_addoption(parser):
    """Register custom CLI options for pytest
    
    Args:
        parser: pytest parser instance
    """
    parser.addoption(
        "--headless",
        action="store",
        default=None,
        help="Run browser in headless mode: true/false",
    )


def pytest_configure(config):
    """Apply CLI overrides to environment variables
    
    Args:
        config: pytest config object
    """
    headless_option = config.getoption("--headless")
    if headless_option is not None:
        os.environ["HEADLESS"] = str(headless_option).lower()
        logger.info("Headless mode set via CLI: %s", headless_option)

    if observability_enabled():
        configure_observability_file_logging()
        init_observability(service_name="qa-portfolio-tests")
        emit_event("observability_initialized")


def pytest_unconfigure(config):
    """Shutdown trace exporter on pytest teardown."""
    if observability_enabled():
        emit_event("observability_shutdown")
        shutdown_observability()



