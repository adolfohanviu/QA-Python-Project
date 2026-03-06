import logging
from typing import Dict, Any, Optional
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError as RequestsConnectionError
from tests.utils.config import config
from tests.utils.observability import current_trace_id, emit_event, traced_span

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
        headers = dict(self.headers)
        trace_id = current_trace_id()
        if trace_id:
            headers["X-Trace-Id"] = trace_id

        logger.info("GET %s", url)
        try:
            with traced_span("api.get", http_url=url, http_method="GET", endpoint=endpoint):
                response = requests.get(url, headers=headers, params=params, timeout=self.timeout)
                self.last_response = response
                logger.info("Status: %s", response.status_code)
                emit_event("api_request", method="GET", endpoint=endpoint, status_code=response.status_code)
                return response
        except (Timeout, RequestsConnectionError) as exc:
            logger.error("Request failed for %s: %s: %s", url, type(exc).__name__, str(exc))
            emit_event("api_request_error", method="GET", endpoint=endpoint, error=str(exc))
            raise
        except RequestException as exc:
            logger.error("Unexpected request error for %s: %s", url, str(exc))
            emit_event("api_request_error", method="GET", endpoint=endpoint, error=str(exc))
            raise
    
    def post(self, endpoint: str, data: Dict[str, Any]) -> requests.Response:
        """POST request"""
        url = f"{self.base_url}{endpoint}"
        headers = dict(self.headers)
        trace_id = current_trace_id()
        if trace_id:
            headers["X-Trace-Id"] = trace_id

        logger.info("POST %s", url)
        try:
            with traced_span("api.post", http_url=url, http_method="POST", endpoint=endpoint):
                response = requests.post(
                    url,
                    headers=headers,
                    json=data,
                    timeout=self.timeout,
                )
                self.last_response = response
                logger.info("Status: %s", response.status_code)
                emit_event("api_request", method="POST", endpoint=endpoint, status_code=response.status_code)
                return response
        except (Timeout, RequestsConnectionError) as exc:
            logger.error("Request failed for %s: %s: %s", url, type(exc).__name__, str(exc))
            emit_event("api_request_error", method="POST", endpoint=endpoint, error=str(exc))
            raise
        except RequestException as exc:
            logger.error("Unexpected request error for %s: %s", url, str(exc))
            emit_event("api_request_error", method="POST", endpoint=endpoint, error=str(exc))
            raise
    
    def put(self, endpoint: str, data: Dict[str, Any]) -> requests.Response:
        """PUT request"""
        url = f"{self.base_url}{endpoint}"
        headers = dict(self.headers)
        trace_id = current_trace_id()
        if trace_id:
            headers["X-Trace-Id"] = trace_id

        logger.info("PUT %s", url)
        try:
            with traced_span("api.put", http_url=url, http_method="PUT", endpoint=endpoint):
                response = requests.put(
                    url,
                    headers=headers,
                    json=data,
                    timeout=self.timeout,
                )
                self.last_response = response
                logger.info("Status: %s", response.status_code)
                emit_event("api_request", method="PUT", endpoint=endpoint, status_code=response.status_code)
                return response
        except (Timeout, RequestsConnectionError) as exc:
            logger.error("Request failed for %s: %s: %s", url, type(exc).__name__, str(exc))
            emit_event("api_request_error", method="PUT", endpoint=endpoint, error=str(exc))
            raise
        except RequestException as exc:
            logger.error("Unexpected request error for %s: %s", url, str(exc))
            emit_event("api_request_error", method="PUT", endpoint=endpoint, error=str(exc))
            raise
    
    def delete(self, endpoint: str) -> requests.Response:
        """DELETE request"""
        url = f"{self.base_url}{endpoint}"
        headers = dict(self.headers)
        trace_id = current_trace_id()
        if trace_id:
            headers["X-Trace-Id"] = trace_id

        logger.info("DELETE %s", url)
        try:
            with traced_span("api.delete", http_url=url, http_method="DELETE", endpoint=endpoint):
                response = requests.delete(url, headers=headers, timeout=self.timeout)
                self.last_response = response
                logger.info("Status: %s", response.status_code)
                emit_event("api_request", method="DELETE", endpoint=endpoint, status_code=response.status_code)
                return response
        except (Timeout, RequestsConnectionError) as exc:
            logger.error("Request failed for %s: %s: %s", url, type(exc).__name__, str(exc))
            emit_event("api_request_error", method="DELETE", endpoint=endpoint, error=str(exc))
            raise
        except RequestException as exc:
            logger.error("Unexpected request error for %s: %s", url, str(exc))
            emit_event("api_request_error", method="DELETE", endpoint=endpoint, error=str(exc))
            raise
    
    def get_json(self) -> Dict:
        """Get JSON response from last request"""
        if not self.last_response:
            raise ValueError("No previous response")
        try:
            return self.last_response.json()
        except ValueError as exc:
            logger.error("Failed to decode JSON response: %s", str(exc))
            raise
    
    def get_status_code(self) -> int:
        """Get status code from last response"""
        if not self.last_response:
            raise ValueError("No previous response")
        return self.last_response.status_code
