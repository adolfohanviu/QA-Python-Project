import logging
import json
from typing import Dict, Any, Optional
import requests
from tests.utils.config import config

logger = logging.getLogger(__name__)


class APIClient:
    """REST API client for testing"""
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or config.api_base_url
        self.headers = {"Content-Type": "application/json"}
        self.last_response = None
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> requests.Response:
        """GET request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"GET {url}")
        response = requests.get(url, headers=self.headers, params=params, timeout=10)
        self.last_response = response
        logger.info(f"Status: {response.status_code}")
        return response
    
    def post(self, endpoint: str, data: Dict[str, Any]) -> requests.Response:
        """POST request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"POST {url} with data: {data}")
        response = requests.post(
            url,
            headers=self.headers,
            json=data,
            timeout=10
        )
        self.last_response = response
        logger.info(f"Status: {response.status_code}")
        return response
    
    def put(self, endpoint: str, data: Dict[str, Any]) -> requests.Response:
        """PUT request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"PUT {url} with data: {data}")
        response = requests.put(
            url,
            headers=self.headers,
            json=data,
            timeout=10
        )
        self.last_response = response
        logger.info(f"Status: {response.status_code}")
        return response
    
    def delete(self, endpoint: str) -> requests.Response:
        """DELETE request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"DELETE {url}")
        response = requests.delete(url, headers=self.headers, timeout=10)
        self.last_response = response
        logger.info(f"Status: {response.status_code}")
        return response
    
    def get_json(self) -> Dict:
        """Get JSON response from last request"""
        if not self.last_response:
            raise ValueError("No previous response")
        return self.last_response.json()
    
    def get_status_code(self) -> int:
        """Get status code from last response"""
        if not self.last_response:
            raise ValueError("No previous response")
        return self.last_response.status_code
