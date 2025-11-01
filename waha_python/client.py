"""
Main WAHA Client implementation
"""

import requests
from typing import Optional, Dict, Any, Union
from .exceptions import (
    WAHAClientError,
    WAHAAuthenticationError,
    WAHANotFoundError,
    WAHARateLimitError,
    WAHAServerError,
)

# Import sub-modules
from .modules.sessions import SessionsModule
from .modules.messages import MessagesModule
from .modules.chats import ChatsModule
from .modules.contacts import ContactsModule
from .modules.groups import GroupsModule
from .modules.status import StatusModule
from .modules.profile import ProfileModule
from .modules.channels import ChannelsModule


class WAHAClient:
    """
    WAHA (WhatsApp HTTP API) Python Client

    This is the main client class that provides a high-level interface
    to interact with the WAHA server.

    Args:
        base_url: Base URL of the WAHA server (default: "http://localhost:3000")
        api_key: API key for authentication (optional)
        timeout: Request timeout in seconds (default: 30)

    Example:
        .. code-block:: python

            from waha_python import WAHAClient

            client = WAHAClient(
                base_url="http://localhost:3000",
                api_key="your-api-key-here"
            )

            # Send a text message
            result = client.messages.send_text(
                session="default",
                chat_id="1234567890@c.us",
                text="Hello, World!"
            )
    """

    def __init__(
        self,
        base_url: str = "http://localhost:3000",
        api_key: Optional[str] = None,
        timeout: int = 30,
    ):
        """
        Initialize the WAHA client

        Args:
            base_url: Base URL of the WAHA server
            api_key: API key for authentication
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

        # Initialize session
        self._session = requests.Session()
        self._setup_session()

        # Initialize sub-modules
        self.sessions = SessionsModule(self)
        self.messages = MessagesModule(self)
        self.chats = ChatsModule(self)
        self.contacts = ContactsModule(self)
        self.groups = GroupsModule(self)
        self.status = StatusModule(self)
        self.profile = ProfileModule(self)
        self.channels = ChannelsModule(self)

    def _setup_session(self):
        """Setup the requests session with default headers and auth"""
        self._session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

        if self.api_key:
            self._session.headers["X-Api-Key"] = self.api_key

    def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Union[Dict[str, Any], Any]:
        """
        Make a request to the WAHA API

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (e.g., "/api/sessions")
            params: URL parameters
            json_data: JSON body data
            **kwargs: Additional arguments for requests

        Returns:
            Response data

        Raises:
            WAHAAuthenticationError: If authentication fails
            WAHANotFoundError: If resource is not found
            WAHARateLimitError: If rate limit is exceeded
            WAHAServerError: If server returns an error
            WAHAClientError: For other errors
        """
        url = f"{self.base_url}{endpoint}"
        timeout = kwargs.pop("timeout", self.timeout)

        try:
            response = self._session.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                timeout=timeout,
                **kwargs
            )
            return self._handle_response(response)
        except requests.exceptions.Timeout as e:
            raise WAHAClientError(f"Request timeout: {e}")
        except requests.exceptions.ConnectionError as e:
            raise WAHAClientError(f"Connection error: {e}")
        except requests.exceptions.RequestException as e:
            raise WAHAClientError(f"Request failed: {e}")

    def _handle_response(self, response: requests.Response) -> Union[Dict[str, Any], Any]:
        """
        Handle the HTTP response

        Args:
            response: HTTP response object

        Returns:
            Response data

        Raises:
            WAHAAuthenticationError: If authentication fails (401)
            WAHANotFoundError: If resource is not found (404)
            WAHARateLimitError: If rate limit is exceeded (429)
            WAHAServerError: If server returns an error (5xx)
        """
        # Handle different status codes
        if response.status_code == 401:
            raise WAHAAuthenticationError(
                "Authentication failed. Please check your API key."
            )
        elif response.status_code == 404:
            raise WAHANotFoundError(f"Resource not found: {response.url}")
        elif response.status_code == 429:
            raise WAHARateLimitError("Rate limit exceeded. Please try again later.")
        elif response.status_code >= 500:
            error_msg = "Server error"
            try:
                error_data = response.json()
                error_msg = error_data.get("message", error_msg)
            except:
                pass
            raise WAHAServerError(f"{error_msg} (Status: {response.status_code})")

        # Handle successful responses
        if response.status_code in [200, 201, 204]:
            # Handle different content types
            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type:
                return response.json()
            elif "image/" in content_type or "application/octet-stream" in content_type:
                return response.content
            else:
                return response.text

        # Handle other error codes
        if response.status_code >= 400:
            error_msg = "Unknown error"
            try:
                error_data = response.json()
                error_msg = error_data.get("message", error_msg)
            except:
                error_msg = response.text
            raise WAHAClientError(f"{error_msg} (Status: {response.status_code})")

        return response.text

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Union[Dict[str, Any], Any]:
        """Make a GET request"""
        return self.request("GET", endpoint, params=params, **kwargs)

    def post(self, endpoint: str, json_data: Optional[Dict[str, Any]] = None, **kwargs) -> Union[Dict[str, Any], Any]:
        """Make a POST request"""
        return self.request("POST", endpoint, json_data=json_data, **kwargs)

    def put(self, endpoint: str, json_data: Optional[Dict[str, Any]] = None, **kwargs) -> Union[Dict[str, Any], Any]:
        """Make a PUT request"""
        return self.request("PUT", endpoint, json_data=json_data, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> Union[Dict[str, Any], Any]:
        """Make a DELETE request"""
        return self.request("DELETE", endpoint, **kwargs)

    def close(self):
        """Close the client session"""
        self._session.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()

