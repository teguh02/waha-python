"""
Messages module for WAHA Python client
"""

from typing import List, Optional, Dict, Any, Union
from ..base_module import BaseModule


class MessagesModule(BaseModule):
    """
    Module for sending and receiving WhatsApp messages
    """

    def send_text(
        self,
        session: str,
        chat_id: str,
        text: str,
        reply_to: Optional[str] = None,
        mentions: Optional[List[str]] = None,
        link_preview: bool = True,
        link_preview_high_quality: bool = False,
    ) -> Dict[str, Any]:
        """
        Send a text message

        Args:
            session: Session name
            chat_id: Chat ID (e.g., "1234567890@c.us")
            text: Message text
            reply_to: Message ID to reply to
            mentions: List of chat IDs to mention (for groups)
            link_preview: Enable link preview (default: True)
            link_preview_high_quality: Enable high-quality link preview (default: False)

        Returns:
            Message result

        Example:
            .. code-block:: python

                result = client.messages.send_text(
                    session="default",
                    chat_id="1234567890@c.us",
                    text="Hello, World!"
                )
        """
        data: Dict[str, Any] = {
            "session": session,
            "chatId": chat_id,
            "text": text,
        }

        if reply_to:
            data["reply_to"] = reply_to
        if mentions:
            data["mentions"] = mentions
        if not link_preview:
            data["linkPreview"] = False
        if link_preview_high_quality:
            data["linkPreviewHighQuality"] = True

        return self.post("/api/sendText", json_data=data)

    def send_seen(
        self,
        session: str,
        chat_id: str,
        message_ids: Optional[List[str]] = None,
        participant: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Mark message(s) as seen

        Args:
            session: Session name
            chat_id: Chat ID
            message_ids: List of message IDs to mark as seen
            participant: Participant ID (for group messages)

        Returns:
            Result

        Example:
            .. code-block:: python

                result = client.messages.send_seen(
                    session="default",
                    chat_id="1234567890@c.us"
                )
        """
        data: Dict[str, Any] = {
            "session": session,
            "chatId": chat_id,
        }

        if message_ids:
            data["messageIds"] = message_ids
        if participant:
            data["participant"] = participant

        return self.post("/api/sendSeen", json_data=data)

    def send_image(
        self,
        session: str,
        chat_id: str,
        file: Union[Dict[str, Any], str],
        caption: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Send an image

        Args:
            session: Session name
            chat_id: Chat ID
            file: File data (dict with url/data/mimetype/filename or file path)
            caption: Image caption (optional)

        Returns:
            Message result

        Example:
            .. code-block:: python

                # Using URL
                result = client.messages.send_image(
                    session="default",
                    chat_id="1234567890@c.us",
                    file={"url": "https://example.com/image.jpg", "mimetype": "image/jpeg"}
                )

                # Using base64 data
                result = client.messages.send_image(
                    session="default",
                    chat_id="1234567890@c.us",
                    file={"data": "base64data...", "mimetype": "image/jpeg", "filename": "image.jpg"}
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

        data: Dict[str, Any] = {
            "session": session,
            "chatId": chat_id,
            "file": file,
        }

        if caption:
            data["caption"] = caption

        return self.post("/api/sendImage", json_data=data)

    def send_video(
        self,
        session: str,
        chat_id: str,
        file: Union[Dict[str, Any], str],
        caption: Optional[str] = None,
        as_note: bool = False,
        convert: bool = False,
    ) -> Dict[str, Any]:
        """
        Send a video

        Args:
            session: Session name
            chat_id: Chat ID
            file: File data (dict with url/data/mimetype/filename or file path)
            caption: Video caption (optional)
            as_note: Send as video note (rounded video)
            convert: Convert video to right format (default: False)

        Returns:
            Message result

        Example:
            .. code-block:: python

                result = client.messages.send_video(
                    session="default",
                    chat_id="1234567890@c.us",
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

        data: Dict[str, Any] = {
            "session": session,
            "chatId": chat_id,
            "file": file,
        }

        if caption:
            data["caption"] = caption
        if as_note:
            data["asNote"] = True
        if convert:
            data["convert"] = True

        return self.post("/api/sendVideo", json_data=data)

    def send_voice(
        self,
        session: str,
        chat_id: str,
        file: Union[Dict[str, Any], str],
        convert: bool = False,
    ) -> Dict[str, Any]:
        """
        Send a voice message

        Args:
            session: Session name
            chat_id: Chat ID
            file: File data (dict with url/data/mimetype/filename or file path)
            convert: Convert voice to right format (default: False)

        Returns:
            Message result

        Example:
            .. code-block:: python

                result = client.messages.send_voice(
                    session="default",
                    chat_id="1234567890@c.us",
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

        data: Dict[str, Any] = {
            "session": session,
            "chatId": chat_id,
            "file": file,
        }

        if convert:
            data["convert"] = True

        return self.post("/api/sendVoice", json_data=data)

    def send_file(
        self,
        session: str,
        chat_id: str,
        file: Union[Dict[str, Any], str],
        caption: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Send a file (document)

        Args:
            session: Session name
            chat_id: Chat ID
            file: File data (dict with url/data/mimetype/filename or file path)
            caption: File caption (optional)

        Returns:
            Message result

        Example:
            .. code-block:: python

                result = client.messages.send_file(
                    session="default",
                    chat_id="1234567890@c.us",
                    file={"url": "https://example.com/file.pdf", "mimetype": "application/pdf"}
                )
        """
        if isinstance(file, str):
            # If file is a string, assume it's a file path
            import base64
            with open(file, "rb") as f:
                data = base64.b64encode(f.read()).decode()
                import mimetypes
                mimetype = mimetypes.guess_type(file)[0] or "application/octet-stream"
                file = {"data": data, "mimetype": mimetype, "filename": file}

        data: Dict[str, Any] = {
            "session": session,
            "chatId": chat_id,
            "file": file,
        }

        if caption:
            data["caption"] = caption

        return self.post("/api/sendFile", json_data=data)

    def send_location(
        self,
        session: str,
        chat_id: str,
        latitude: float,
        longitude: float,
        title: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Send a location

        Args:
            session: Session name
            chat_id: Chat ID
            latitude: Latitude
            longitude: Longitude
            title: Location title (optional)

        Returns:
            Message result

        Example:
            .. code-block:: python

                result = client.messages.send_location(
                    session="default",
                    chat_id="1234567890@c.us",
                    latitude=38.8937255,
                    longitude=-77.0969763,
                    title="Our office"
                )
        """
        data: Dict[str, Any] = {
            "session": session,
            "chatId": chat_id,
            "latitude": latitude,
            "longitude": longitude,
        }

        if title:
            data["title"] = title

        return self.post("/api/sendLocation", json_data=data)

    def send_contact(
        self,
        session: str,
        chat_id: str,
        contacts: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Send contact(s) (vCard)

        Args:
            session: Session name
            chat_id: Chat ID
            contacts: List of contact dictionaries

        Returns:
            Message result

        Example:
            .. code-block:: python

                result = client.messages.send_contact(
                    session="default",
                    chat_id="1234567890@c.us",
                    contacts=[{
                        "fullName": "John Doe",
                        "organization": "Company Name",
                        "phoneNumber": "+91 11111 11111",
                        "whatsappId": "911111111111"
                    }]
                )
        """
        data: Dict[str, Any] = {
            "session": session,
            "chatId": chat_id,
            "contacts": contacts,
        }

        return self.post("/api/sendContactVcard", json_data=data)

    def send_poll(
        self,
        session: str,
        chat_id: str,
        poll: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Send a poll

        Args:
            session: Session name
            chat_id: Chat ID
            poll: Poll data (name, options, multipleAnswers)

        Returns:
            Message result

        Example:
            .. code-block:: python

                result = client.messages.send_poll(
                    session="default",
                    chat_id="1234567890@c.us",
                    poll={
                        "name": "How are you?",
                        "options": ["Awesome!", "Good!", "Not bad!"],
                        "multipleAnswers": False
                    }
                )
        """
        data: Dict[str, Any] = {
            "session": session,
            "chatId": chat_id,
            "poll": poll,
        }

        return self.post("/api/sendPoll", json_data=data)

    def forward_message(
        self,
        session: str,
        chat_id: str,
        message_id: str,
    ) -> Dict[str, Any]:
        """
        Forward a message

        Args:
            session: Session name
            chat_id: Chat ID to forward to
            message_id: Message ID to forward

        Returns:
            Message result

        Example:
            .. code-block:: python

                result = client.messages.forward_message(
                    session="default",
                    chat_id="1234567890@c.us",
                    message_id="false_1234567890@c.us_AAAAAAAAAAAAAAAAAA"
                )
        """
        data: Dict[str, Any] = {
            "session": session,
            "chatId": chat_id,
            "messageId": message_id,
        }

        return self.post("/api/forwardMessage", json_data=data)

    def add_reaction(
        self,
        session: str,
        message_id: str,
        reaction: str,
    ) -> Dict[str, Any]:
        """
        Add a reaction to a message

        Args:
            session: Session name
            message_id: Message ID
            reaction: Reaction emoji (use "" to remove)

        Returns:
            Result

        Example:
            .. code-block:: python

                # Add reaction
                result = client.messages.add_reaction(
                    session="default",
                    message_id="false_1234567890@c.us_AAAAAAAAAAAAAAAAAA",
                    reaction="👍"
                )

                # Remove reaction
                result = client.messages.add_reaction(
                    session="default",
                    message_id="false_1234567890@c.us_AAAAAAAAAAAAAAAAAA",
                    reaction=""
                )
        """
        data: Dict[str, Any] = {
            "session": session,
            "messageId": message_id,
            "reaction": reaction,
        }

        return self.put("/api/reaction", json_data=data)

    def star_message(
        self,
        session: str,
        chat_id: str,
        message_id: str,
        star: bool = True,
    ) -> Dict[str, Any]:
        """
        Star or unstar a message

        Args:
            session: Session name
            chat_id: Chat ID
            message_id: Message ID
            star: True to star, False to unstar (default: True)

        Returns:
            Result

        Example:
            .. code-block:: python

                result = client.messages.star_message(
                    session="default",
                    chat_id="1234567890@c.us",
                    message_id="false_1234567890@c.us_AAAAAAAAAAAAAAAAAA"
                )
        """
        data: Dict[str, Any] = {
            "session": session,
            "chatId": chat_id,
            "messageId": message_id,
            "star": star,
        }

        return self.put("/api/star", json_data=data)

    def edit_message(
        self,
        session: str,
        chat_id: str,
        message_id: str,
        text: str,
        link_preview: bool = True,
    ) -> Dict[str, Any]:
        """
        Edit a message

        Args:
            session: Session name
            chat_id: Chat ID
            message_id: Message ID
            text: New text
            link_preview: Enable link preview (default: True)

        Returns:
            Result

        Example:
            .. code-block:: python

                result = client.messages.edit_message(
                    session="default",
                    chat_id="1234567890@c.us",
                    message_id="false_1234567890@c.us_AAAAAAAAAAAAAAAAAA",
                    text="Updated message"
                )
        """
        data: Dict[str, Any] = {"text": text}
        if not link_preview:
            data["linkPreview"] = False

        return self.put(
            f"/api/{session}/chats/{chat_id}/messages/{message_id}", json_data=data
        )

    def delete_message(
        self,
        session: str,
        chat_id: str,
        message_id: str,
    ) -> Dict[str, Any]:
        """
        Delete a message

        Args:
            session: Session name
            chat_id: Chat ID
            message_id: Message ID

        Returns:
            Result

        Example:
            .. code-block:: python

                result = client.messages.delete_message(
                    session="default",
                    chat_id="1234567890@c.us",
                    message_id="false_1234567890@c.us_AAAAAAAAAAAAAAAAAA"
                )
        """
        return self.request(
            "DELETE", f"/api/{session}/chats/{chat_id}/messages/{message_id}"
        )

    def pin_message(
        self,
        session: str,
        chat_id: str,
        message_id: str,
    ) -> Dict[str, Any]:
        """
        Pin a message

        Args:
            session: Session name
            chat_id: Chat ID
            message_id: Message ID

        Returns:
            Result

        Example:
            .. code-block:: python

                result = client.messages.pin_message(
                    session="default",
                    chat_id="1234567890@c.us",
                    message_id="false_1234567890@c.us_AAAAAAAAAAAAAAAAAA"
                )
        """
        return self.post(
            f"/api/{session}/chats/{chat_id}/messages/{message_id}/pin"
        )

    def unpin_message(
        self,
        session: str,
        chat_id: str,
        message_id: str,
    ) -> Dict[str, Any]:
        """
        Unpin a message

        Args:
            session: Session name
            chat_id: Chat ID
            message_id: Message ID

        Returns:
            Result

        Example:
            .. code-block:: python

                result = client.messages.unpin_message(
                    session="default",
                    chat_id="1234567890@c.us",
                    message_id="false_1234567890@c.us_AAAAAAAAAAAAAAAAAA"
                )
        """
        return self.post(
            f"/api/{session}/chats/{chat_id}/messages/{message_id}/unpin"
        )

