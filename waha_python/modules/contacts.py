"""
Contacts module for WAHA Python client
"""

from typing import List, Dict, Any, Optional
from ..base_module import BaseModule


class ContactsModule(BaseModule):
    """
    Module for managing WhatsApp contacts
    """

    def list_all(
        self,
        session: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get all contacts

        Args:
            session: Session name
            limit: Limit number of results
            offset: Skip number of results
            sort_by: Sort by field (id, name)
            sort_order: Sort order (asc, desc)

        Returns:
            List of contacts

        Example:
            .. code-block:: python

                contacts = client.contacts.list_all("default")
        """
        params = {"session": session}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if sort_by:
            params["sortBy"] = sort_by
        if sort_order:
            params["sortOrder"] = sort_order

        return self.get("/api/contacts/all", params=params)

    def get_contact(self, session: str, contact_id: str) -> Dict[str, Any]:
        """
        Get a specific contact

        Args:
            session: Session name
            contact_id: Contact ID (phone number or chat ID)

        Returns:
            Contact data

        Example:
            .. code-block:: python

                contact = client.contacts.get_contact("default", "1234567890")
        """
        params = {"session": session, "contactId": contact_id}
        return self.request("GET", "/api/contacts", params=params)

    def update(
        self, session: str, chat_id: str, first_name: str, last_name: str
    ) -> Dict[str, Any]:
        """
        Update a contact

        Args:
            session: Session name
            chat_id: Chat ID
            first_name: First name
            last_name: Last name

        Returns:
            Result

        Example:
            .. code-block:: python

                result = client.contacts.update(
                    "default", "1234567890@c.us", "John", "Doe"
                )
        """
        data = {"firstName": first_name, "lastName": last_name}
        return self.put(f"/api/{session}/contacts/{chat_id}", json_data=data)

    def check_exists(self, session: str, phone: str) -> Dict[str, Any]:
        """
        Check if a phone number exists in WhatsApp

        Args:
            session: Session name
            phone: Phone number

        Returns:
            Result with numberExists and chatId fields

        Example:
            .. code-block:: python

                result = client.contacts.check_exists("default", "1234567890")
                if result["numberExists"]:
                    print(f"Chat ID: {result['chatId']}")
        """
        params = {"session": session, "phone": phone}
        return self.get("/api/contacts/check-exists", params=params)

    def get_about(self, session: str, contact_id: str) -> Dict[str, Any]:
        """
        Get contact's "about" information

        Args:
            session: Session name
            contact_id: Contact ID

        Returns:
            About information

        Example:
            .. code-block:: python

                about = client.contacts.get_about("default", "1234567890")
        """
        params = {"session": session, "contactId": contact_id}
        return self.get("/api/contacts/about", params=params)

    def get_profile_picture(
        self, session: str, contact_id: str, refresh: bool = False
    ) -> Dict[str, Any]:
        """
        Get contact's profile picture

        Args:
            session: Session name
            contact_id: Contact ID
            refresh: Force refresh the picture

        Returns:
            Profile picture URL

        Example:
            .. code-block:: python

                pic = client.contacts.get_profile_picture("default", "1234567890")
        """
        params = {"session": session, "contactId": contact_id}
        if refresh:
            params["refresh"] = True
        return self.get("/api/contacts/profile-picture", params=params)

    def block(self, session: str, chat_id: str) -> Dict[str, Any]:
        """
        Block a contact

        Args:
            session: Session name
            chat_id: Chat ID

        Returns:
            Result

        Example:
            .. code-block:: python

                result = client.contacts.block("default", "1234567890@c.us")
        """
        data = {"session": session, "chatId": chat_id}
        return self.post("/api/contacts/block", json_data=data)

    def unblock(self, session: str, chat_id: str) -> Dict[str, Any]:
        """
        Unblock a contact

        Args:
            session: Session name
            chat_id: Chat ID

        Returns:
            Result

        Example:
            .. code-block:: python

                result = client.contacts.unblock("default", "1234567890@c.us")
        """
        data = {"session": session, "chatId": chat_id}
        return self.post("/api/contacts/unblock", json_data=data)

