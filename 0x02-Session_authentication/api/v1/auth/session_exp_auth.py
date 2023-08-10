#!/usr/bin/env python3
"""
Define the SessionExpAuth class that enhances SessionAuth by adding session expiration functionality
"""
import os
from datetime import (
    datetime,
    timedelta
)

from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    Extension of the SessionAuth class with session expiration capabilities
    """
    def __init__(self):
        """
        Initialize the class and set session duration
        """
        try:
            duration = int(os.getenv('SESSION_DURATION'))
        except Exception:
            duration = 0
        self.session_duration = duration

    def create_session(self, user_id=None):
        """
        Create a new Session ID for a given user ID
        Args:
            user_id (str): User ID
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_details = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_details
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve the user ID associated with a session ID, considering session expiration
        Args:
            session_id (str): Session ID
        Return:
            User ID or None if session_id is None or invalid
        """
        if session_id is None:
            return None
        user_details = self.user_id_by_session_id.get(session_id)
        if user_details is None or "created_at" not in user_details.keys():
            return None
        if self.session_duration <= 0:
            return user_details.get("user_id")
        created_at = user_details.get("created_at")
        allowed_window = created_at + timedelta(seconds=self.session_duration)
        if allowed_window < datetime.now():
            return None
        return user_details.get("user_id")
