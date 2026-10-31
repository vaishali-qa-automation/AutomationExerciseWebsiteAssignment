import logging
import time
from typing import Any, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = (5, 30)  # (connect, read) seconds

class BaseClient:
    def __init__(self, base_url: str, timeout=DEFAULT_TIMEOUT, headers: Optional[dict] = None):
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._session = requests.Session()
        if headers:
            self._session.headers.update(headers)

        retry_strategy = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=frozenset(["GET", "PUT", "DELETE"]),  # POST is not retried
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self._session.mount("https://", adapter)
        self._session.mount("http://", adapter)

    def _request(self, method, endpoint, headers=None, **kwargs):
        url = f"{self._base_url}/{endpoint.lstrip('/')}"
        kwargs.setdefault("timeout", self._timeout)

        logger.info(f"Request: {method} {url}")
        response = self._session.request(method, url, headers=headers, **kwargs)
        logger.info(f"Response: {method} {url} -> {response.status_code}" )
        logger.debug(f"Response body: {response.text}")
        return response

    def send(self, method, endpoint, **kwargs):
        return self._request(method, endpoint, **kwargs)

    def get(self, endpoint, params=None, headers=None, **kwargs):
        return self._request("GET", endpoint, headers=headers, params=params, **kwargs)

    def post(self, endpoint, data=None, json=None, headers=None, **kwargs):
        return self._request("POST", endpoint, headers=headers, data=data, json=json, **kwargs)

    def put(self, endpoint, data=None, json=None, headers=None, **kwargs):
        return self._request("PUT", endpoint, headers=headers, data=data, json=json, **kwargs)

    def delete(self, endpoint, data=None, headers=None, **kwargs):
        return self._request("DELETE", endpoint, headers=headers, data=data, **kwargs)

    def close(self):
        self._session.close()
