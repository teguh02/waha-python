"""
WAHA Python - Unofficial WhatsApp HTTP API Client

A complete, unofficial Python implementation for WAHA (WhatsApp HTTP API) that provides
a simple and intuitive interface to interact with WhatsApp through the WAHA server.

Features:
    - Session Management (Create, Start, Stop, Restart, Delete sessions)
    - Authentication (QR Code, Pairing Code)
    - Send Messages (Text, Image, Video, Voice, File, Location, Contact)
    - Receive Messages (Webhooks, Events)
    - Chats Management
    - Contacts Management
    - Groups Management
    - Status Management
    - Channels Management
    - Profile Management
    - And much more!

Example:
    Basic usage::

        from waha_python import WAHAClient

        client = WAHAClient(
            base_url="http://localhost:3000",
            api_key="your-api-key"
        )

        # Send a text message
        result = client.messages.send_text(
            session="default",
            chat_id="1234567890@c.us",
            text="Hello, World!"
        )

        # Get all sessions
        sessions = client.sessions.list()
"""

__version__ = "1.0.0"
__author__ = "Teguh Rijanandi"
__license__ = "MIT"

from .client import WAHAClient
from .exceptions import (
    WAHAClientError,
    WAHAAuthenticationError,
    WAHASessionError,
    WAHANotFoundError,
    WAHARateLimitError,
    WAHAServerError,
)

__all__ = [
    "WAHAClient",
    "WAHAClientError",
    "WAHAAuthenticationError",
    "WAHASessionError",
    "WAHANotFoundError",
    "WAHARateLimitError",
    "WAHAServerError",
]

