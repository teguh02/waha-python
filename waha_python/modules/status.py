"""
Status module for WAHA Python client
"""

from typing import Dict, Any, Optional, Union
from ..base_module import BaseModule


class StatusModule(BaseModule):
    """
    Module for managing WhatsApp Status (Stories)
    """

    def send_text(
        self, session: str, text: str
    ) -> Dict[str, Any]:
        """
        Send a text status

        Args:
            session: Session name
            text: Status text

        Returns:
            Status result

        Example:
            .. code-block:: python

                result = client.status.send_text("default", "My status update")
        """
        data = {"text": text}
        return self.post(f"/api/{session}/status/text", json_data=data)

    def send_image(
        self, session: str, file: Union[Dict[str, Any], str], caption: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send an image status

        Args:
            session: Session name
            file: File data (dict with url/data/mimetype/filename or file path)
            caption: Image caption (optional)

        Returns:
            Status result

        Example:
            .. code-block:: python

                result = client.status.send_image(
                    "default",
                    file={"url": "https://example.com/image.jpg", "mimetype": "image/jpeg"}
                )
        """
        if isinstance(file, str):
            # If file is a string, assume it's a file path
            import base64
            with open(file, "rb") as f:
                data = base64.b64encode(f.read()).decode()
                import mimetypes
                mimetype = mimetypes.guess_type(file)[0] or "image/jpeg"
                file = {"data": data, "mimetype": mimetype, "filename": file}

        data: Dict[str, Any] = {"file": file}
        if caption:
            data["caption"] = caption

        return self.post(f"/api/{session}/status/image", json_data=data)

    def send_voice(
        self, session: str, file: Union[Dict[str, Any], str]
    ) -> Dict[str, Any]:
        """
        Send a voice status

        Args:
            session: Session name
            file: File data (dict with url/data/mimetype/filename or file path)

        Returns:
            Status result

        Example:
            .. code-block:: python

                result = client.status.send_voice(
                    "default",
                    file={"url": "https://example.com/voice.opus", "mimetype": "audio/ogg; codecs=opus"}
                )
        """
        if isinstance(file, str):
            # If file is a string, assume it's a file path
            import base64
            with open(file, "rb") as f:
                data = base64.b64encode(f.read()).decode()
                import mimetypes
                mimetype = mimetypes.guess_type(file)[0] or "audio/ogg; codecs=opus"
                file = {"data": data, "mimetype": mimetype, "filename": file}

        data = {"file": file}
        return self.post(f"/api/{session}/status/voice", json_data=data)

    def send_video(
        self, session: str, file: Union[Dict[str, Any], str], caption: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send a video status

        Args:
            session: Session name
            file: File data (dict with url/data/mimetype/filename or file path)
            caption: Video caption (optional)

        Returns:
            Status result

        Example:
            .. code-block:: python

                result = client.status.send_video(
                    "default",
                    file={"url": "https://example.com/video.mp4", "mimetype": "video/mp4"}
                )
        """
        if isinstance(file, str):
            # If file is a string, assume it's a file path
            import base64
            with open(file, "rb") as f:
                data = base64.b64encode(f.read()).decode()
                import mimetypes
                mimetype = mimetypes.guess_type(file)[0] or "video/mp4"
                file = {"data": data, "mimetype": mimetype, "filename": file}

        data: Dict[str, Any] = {"file": file}
        if caption:
            data["caption"] = caption

        return self.post(f"/api/{session}/status/video", json_data=data)

    def delete(
        self, session: str, message_id: str
    ) -> Dict[str, Any]:
        """
        Delete a status

        Args:
            session: Session name
            message_id: Status message ID

        Returns:
            Result

        Example:
            .. code-block:: python

                result = client.status.delete("default", "message_id_here")
        """
        data = {"messageId": message_id}
        return self.post(f"/api/{session}/status/delete", json_data=data)

    def get_new_message_id(self, session: str) -> Dict[str, Any]:
        """
        Get new status message ID

        Args:
            session: Session name

        Returns:
            New message ID

        Example:
            .. code-block:: python

                message_id = client.status.get_new_message_id("default")
        """
        return self.get(f"/api/{session}/status/new-message-id")

