import logging

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = (5, 30)  # (connect, read) seconds
SENSITIVE_KEYS = {"password"}
MAX_BODY_LOG_LENGTH = 1000


def _mask(data):
    """Return a copy of dict data with sensitive values hidden (for logging only)."""
    if not isinstance(data, dict):
        return data
    return {
        key: ("***" if str(key).lower() in SENSITIVE_KEYS else value)
        for key, value in data.items()
    }


class BaseClient:
    def __init__(
        self, base_url: str, timeout=DEFAULT_TIMEOUT, headers: dict | None = None
    ):
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._session = requests.Session()

        if headers:
            # This API expects form data, so a JSON Content-Type would break requests.
            safe_headers = {
                key: value
                for key, value in headers.items()
                if key.lower() != "content-type"
            }
            if len(safe_headers) != len(headers):
                logger.warning(
                    "Ignoring Content-Type header; form data requires "
                    "requests to set it automatically."
                )
            self._session.headers.update(safe_headers)

        retry_strategy = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=frozenset(["GET", "PUT"]),  # POST is not retried
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self._session.mount("https://", adapter)
        self._session.mount("http://", adapter)

    def _request(self, method, endpoint, headers=None, **kwargs):
        url = f"{self._base_url}/{endpoint.lstrip('/')}"
        kwargs.setdefault("timeout", self._timeout)

        logger.info(f"Request: {method} {url}")
        if kwargs.get("params"):
            logger.debug(f"Request params: {_mask(kwargs['params'])}")
        if kwargs.get("data"):
            logger.debug(f"Request data: {_mask(kwargs['data'])}")

        response = self._session.request(method, url, headers=headers, **kwargs)

        logger.info(f"Response: {method} {url} -> {response.status_code}")
        body = response.text
        if len(body) > MAX_BODY_LOG_LENGTH:
            body = f"{body[:MAX_BODY_LOG_LENGTH]}... [truncated]"
        logger.debug(f"Response body: {body}")
        return response

    def send(self, method, endpoint, **kwargs):
        return self._request(method, endpoint, **kwargs)

    def get(self, endpoint, params=None, headers=None, **kwargs):
        return self._request("GET", endpoint, headers=headers, params=params, **kwargs)

    def post(self, endpoint, data=None, headers=None, **kwargs):
        return self._request("POST", endpoint, headers=headers, data=data, **kwargs)

    def put(self, endpoint, data=None, headers=None, **kwargs):
        return self._request("PUT", endpoint, headers=headers, data=data, **kwargs)

    def delete(self, endpoint, data=None, headers=None, **kwargs):
        return self._request("DELETE", endpoint, headers=headers, data=data, **kwargs)

    @staticmethod
    def body_code(response) -> int | None:
        """Return the 'responseCode' from the JSON body, or None if it isn't valid JSON."""
        try:
            return response.json().get("responseCode")
        except (ValueError, AttributeError):
            return None

    def close(self):
        logger.info("Closing request session")
        self._session.close()