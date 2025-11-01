"""
Channels module for WAHA Python client
"""

from typing import List, Dict, Any, Optional
from ..base_module import BaseModule


class ChannelsModule(BaseModule):
    """
    Module for managing WhatsApp Channels
    """

    def list(self, session: str) -> List[Dict[str, Any]]:
        """
        List all channels

        Args:
            session: Session name

        Returns:
            List of channels

        Example:
            .. code-block:: python

                channels = client.channels.list("default")
        """
        return self.get(f"/api/{session}/channels")

    def get(self, session: str, channel_id: str) -> Dict[str, Any]:
        """
        Get a specific channel

        Args:
            session: Session name
            channel_id: Channel ID

        Returns:
            Channel data

        Example:
            .. code-block:: python

                channel = client.channels.get("default", "channel_id_here")
        """
        return self.request("GET", f"/api/{session}/channels/{channel_id}")

    def create(
        self, session: str, name: str, description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new channel

        Args:
            session: Session name
            name: Channel name
            description: Channel description (optional)

        Returns:
            Created channel data

        Example:
            .. code-block:: python

                channel = client.channels.create("default", "My Channel")
        """
        data: Dict[str, Any] = {"name": name}
        if description:
            data["description"] = description

        return self.post(f"/api/{session}/channels", json_data=data)

    def delete(self, session: str, channel_id: str) -> Dict[str, Any]:
        """
        Delete a channel

        Args:
            session: Session name
            channel_id: Channel ID

        Returns:
            Result

        Example:
            .. code-block:: python

                result = client.channels.delete("default", "channel_id_here")
        """
        return self.request("DELETE", f"/api/{session}/channels/{channel_id}")

    def get_messages(
        self, session: str, channel_id: str, limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get messages from a channel

        Args:
            session: Session name
            channel_id: Channel ID
            limit: Limit number of messages

        Returns:
            List of messages

        Example:
            .. code-block:: python

                messages = client.channels.get_messages("default", "channel_id_here")
        """
        params = {}
        if limit is not None:
            params["limit"] = limit

        return self.get(
            f"/api/{session}/chats/{channel_id}/messages",
            params=params if params else None,
        )

