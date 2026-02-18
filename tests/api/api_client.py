import logging
import json
from typing import Dict, Any, Optional
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError
from tests.utils.config import config

logger = logging.getLogger(__name__)


class APIClient:
    """REST API client for testing"""
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or config.api_base_url
        self.headers = {"Content-Type": "application/json"}
        self.last_response = None
        self.timeout = 10
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> requests.Response:
        """GET request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"GET {url}")
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=self.timeout)
            self.last_response = response
            logger.info(f"Status: {response.status_code}")
            return response
        except (Timeout, ConnectionError) as e:
            logger.error(f"Request failed for {url}: {type(e).__name__}: {str(e)}")
            raise
        except RequestException as e:
            logger.error(f"Unexpected request error for {url}: {str(e)}")
            raise
    
    def post(self, endpoint: str, data: Dict[str, Any]) -> requests.Response:
        """POST request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"POST {url}")
        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=data,
                timeout=self.timeout
            )
            self.last_response = response
            logger.info(f"Status: {response.status_code}")
            return response
        except (Timeout, ConnectionError) as e:
            logger.error(f"Request failed for {url}: {type(e).__name__}: {str(e)}")
            raise
        except RequestException as e:
            logger.error(f"Unexpected request error for {url}: {str(e)}")
            raise
    
    def put(self, endpoint: str, data: Dict[str, Any]) -> requests.Response:
        """PUT request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"PUT {url}")
        try:
            response = requests.put(
                url,
                headers=self.headers,
                json=data,
                timeout=self.timeout
            )
            self.last_response = response
            logger.info(f"Status: {response.status_code}")
            return response
        except (Timeout, ConnectionError) as e:
            logger.error(f"Request failed for {url}: {type(e).__name__}: {str(e)}")
            raise
        except RequestException as e:
            logger.error(f"Unexpected request error for {url}: {str(e)}")
            raise
    
    def delete(self, endpoint: str) -> requests.Response:
        """DELETE request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"DELETE {url}")
        try:
            response = requests.delete(url, headers=self.headers, timeout=self.timeout)
            self.last_response = response
            logger.info(f"Status: {response.status_code}")
            return response
        except (Timeout, ConnectionError) as e:
            logger.error(f"Request failed for {url}: {type(e).__name__}: {str(e)}")
            raise
        except RequestException as e:
            logger.error(f"Unexpected request error for {url}: {str(e)}")
            raise
    
    def get_json(self) -> Dict:
        """Get JSON response from last request"""
        if not self.last_response:
            raise ValueError("No previous response")
        try:
            return self.last_response.json()
        except ValueError as e:
            logger.error(f"Failed to decode JSON response: {str(e)}")
            raise
    
    def get_status_code(self) -> int:
        """Get status code from last response"""
        if not self.last_response:
            raise ValueError("No previous response")
        return self.last_response.status_code
