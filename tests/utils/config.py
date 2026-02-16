import os
import logging
from functools import lru_cache
from typing import Dict, Any
from dotenv import load_dotenv
import json

load_dotenv()
logger = logging.getLogger(__name__)


class Config:
    """Application configuration management"""
    
    def __init__(self):
        self.base_url = os.getenv("BASE_URL", "https://www.saucedemo.com")
        self.api_base_url = os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")
        self.headless = os.getenv("HEADLESS", "true").lower() != "false"
        self.browser_type = os.getenv("BROWSER_TYPE", "chromium")
        self.timeout = int(os.getenv("TIMEOUT", "30000"))
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        
        logger.info(f"Config loaded: BASE_URL={self.base_url}, HEADLESS={self.headless}")
    
    @staticmethod
    def load_fixture(fixture_name: str) -> Dict[str, Any]:
        """Load test data fixture from JSON"""
        fixture_path = os.path.join(
            os.path.dirname(__file__),
            "fixtures",
            "api_users.json"
        )
        
        with open(fixture_path, "r") as f:
            fixtures = json.load(f)
        
        if fixture_name not in fixtures:
            raise ValueError(f"Fixture '{fixture_name}' not found in {fixture_path}")
        
        return fixtures[fixture_name]


config = Config()
