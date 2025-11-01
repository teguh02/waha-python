"""
Base module class for WAHA Python client
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import WAHAClient


class BaseModule:
    """
    Base class for all WAHA modules

    Provides common functionality for sub-modules
    """

    def __init__(self, client: "WAHAClient"):
        """
        Initialize the module

        Args:
            client: WAHA client instance
        """
        self.client = client

    def request(self, *args, **kwargs):
        """
        Proxy method to client request

        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Response data
        """
        return self.client.request(*args, **kwargs)

    def get(self, *args, **kwargs):
        """Proxy method to client get"""
        return self.client.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        """Proxy method to client post"""
        return self.client.post(*args, **kwargs)

    def put(self, *args, **kwargs):
        """Proxy method to client put"""
        return self.client.put(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Proxy method to client delete"""
        return self.client.delete(*args, **kwargs)

