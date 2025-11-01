"""
Sessions module for WAHA Python client
"""

from typing import List, Dict, Any, Optional
from ..base_module import BaseModule


class SessionsModule(BaseModule):
    """
    Module for managing WAHA sessions

    A session represents a WhatsApp account connected to WAHA
    """

    def list(self, all_sessions: bool = False) -> List[Dict[str, Any]]:
        """
        List all sessions

        Args:
            all_sessions: If True, returns all sessions including STOPPED ones

        Returns:
            List of session information

        Example:
            .. code-block:: python

                # List active sessions
                sessions = client.sessions.list()

                # List all sessions including stopped ones
                all_sessions = client.sessions.list(all_sessions=True)
        """
        params = {"all": all_sessions} if all_sessions else None
        return self.get("/api/sessions", params=params)

    def get(self, session_name: str) -> Dict[str, Any]:
        """
        Get session information

        Args:
            session_name: Name of the session

        Returns:
            Session information

        Example:
            .. code-block:: python

                session = client.sessions.get("default")
        """
        return self.request("GET", f"/api/sessions/{session_name}")

    def create(
        self,
        name: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
        start: bool = True,
    ) -> Dict[str, Any]:
        """
        Create a new session

        Args:
            name: Session name (optional, will be auto-generated if not provided)
            config: Session configuration (optional)
            start: Whether to start the session immediately (default: True)

        Returns:
            Created session information

        Example:
            .. code-block:: python

                # Create and start a session
                session = client.sessions.create(
                    name="my_session",
                    config={"webhooks": [{"url": "https://example.com/webhook", "events": ["message"]}]}
                )

                # Create without starting
                session = client.sessions.create(
                    name="my_session",
                    start=False
                )
        """
        data: Dict[str, Any] = {}
        if name:
            data["name"] = name
        if config:
            data["config"] = config
        if not start:
            data["start"] = False

        return self.post("/api/sessions", json_data=data)

    def update(
        self, session_name: str, config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update session configuration

        Args:
            session_name: Name of the session
            config: New configuration (full config required)

        Returns:
            Updated session information

        Example:
            .. code-block:: python

                session = client.sessions.update(
                    "my_session",
                    {"webhooks": [{"url": "https://example.com/webhook", "events": ["message"]}]}
                )
        """
        data = {"name": session_name, "config": config}
        return self.request("PUT", f"/api/sessions/{session_name}", json_data=data)

    def start(self, session_name: str) -> Dict[str, Any]:
        """
        Start a session

        Args:
            session_name: Name of the session

        Returns:
            Session information

        Example:
            .. code-block:: python

                session = client.sessions.start("my_session")
        """
        return self.post(f"/api/sessions/{session_name}/start")

    def stop(self, session_name: str) -> Dict[str, Any]:
        """
        Stop a session

        Args:
            session_name: Name of the session

        Returns:
            Session information

        Example:
            .. code-block:: python

                session = client.sessions.stop("my_session")
        """
        return self.post(f"/api/sessions/{session_name}/stop")

    def restart(self, session_name: str) -> Dict[str, Any]:
        """
        Restart a session

        Args:
            session_name: Name of the session

        Returns:
            Session information

        Example:
            .. code-block:: python

                session = client.sessions.restart("my_session")
        """
        return self.post(f"/api/sessions/{session_name}/restart")

    def logout(self, session_name: str) -> Dict[str, Any]:
        """
        Logout from a session

        Args:
            session_name: Name of the session

        Returns:
            Logout result

        Example:
            .. code-block:: python

                result = client.sessions.logout("my_session")
        """
        return self.post(f"/api/sessions/{session_name}/logout")

    def delete(self, session_name: str) -> Dict[str, Any]:
        """
        Delete a session

        Args:
            session_name: Name of the session

        Returns:
            Delete result

        Example:
            .. code-block:: python

                result = client.sessions.delete("my_session")
        """
        return self.request("DELETE", f"/api/sessions/{session_name}")

    def get_me(self, session_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about the associated account for the session

        Args:
            session_name: Name of the session

        Returns:
            Account information or None if not authenticated

        Example:
            .. code-block:: python

                me = client.sessions.get_me("default")
                if me:
                    print(f"Logged in as: {me['pushName']}")
        """
        return self.get(f"/api/sessions/{session_name}/me")

    def get_qr(
        self,
        session_name: str,
        format: str = "image",
        accept_json: bool = False,
    ) -> Any:
        """
        Get QR code for pairing WhatsApp

        Args:
            session_name: Name of the session
            format: QR format ('image' or 'raw')
            accept_json: If True, returns JSON with base64 data

        Returns:
            QR code data (binary, base64, or raw value)

        Example:
            .. code-block:: python

                # Get QR code as image
                qr_image = client.sessions.get_qr("default")

                # Get QR code as base64
                qr_data = client.sessions.get_qr("default", accept_json=True)

                # Get QR code raw value
                qr_value = client.sessions.get_qr("default", format="raw")
        """
        endpoint = f"/api/{session_name}/auth/qr"
        params = {"format": format}

        if accept_json or format == "raw":
            # Request JSON response
            response = self.request(
                "GET", endpoint, params=params
            )
            return response

        # Request binary image
        return self.client.request("GET", endpoint, params=params)

    def request_code(
        self, session_name: str, phone_number: str
    ) -> Dict[str, Any]:
        """
        Request authentication code for pairing

        Args:
            session_name: Name of the session
            phone_number: Phone number to pair with

        Returns:
            Pairing code information

        Example:
            .. code-block:: python

                result = client.sessions.request_code("default", "12132132130")
                print(f"Pairing code: {result['code']}")
        """
        data = {"phoneNumber": phone_number}
        return self.post(f"/api/{session_name}/auth/request-code", json_data=data)

    def get_screenshot(
        self, session_name: str, accept_json: bool = False
    ) -> Any:
        """
        Get screenshot of the session

        Args:
            session_name: Name of the session
            accept_json: If True, returns JSON with base64 data

        Returns:
            Screenshot data (binary or base64)

        Example:
            .. code-block:: python

                # Get screenshot as image
                screenshot = client.sessions.get_screenshot("default")

                # Get screenshot as base64
                screenshot_data = client.sessions.get_screenshot("default", accept_json=True)
        """
        endpoint = f"/api/screenshot"
        params = {"session": session_name}

        if accept_json:
            headers = {"Accept": "application/json"}
            response = self.client.request(
                "GET", endpoint, params=params, headers=headers
            )
            return response

        return self.client.request("GET", endpoint, params=params)

