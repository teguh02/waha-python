"""
Exception classes for WAHA Python client
"""


class WAHAClientError(Exception):
    """Base exception for all WAHA client errors"""

    pass


class WAHAAuthenticationError(WAHAClientError):
    """Raised when authentication fails"""

    pass


class WAHASessionError(WAHAClientError):
    """Raised when session operation fails"""

    pass


class WAHANotFoundError(WAHAClientError):
    """Raised when a resource is not found"""

    pass


class WAHARateLimitError(WAHAClientError):
    """Raised when rate limit is exceeded"""

    pass


class WAHAServerError(WAHAClientError):
    """Raised when server returns an error"""

    pass

