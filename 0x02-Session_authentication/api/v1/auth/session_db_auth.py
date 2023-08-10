#!/usr/bin/env python3
"""
Define the SessionDBAuth class that manages session data using a database
"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    Extended class SessionDBAuth that stores session data in a database
    """

    def create_session(self, user_id=None):
        """
        Create a new session for a given user ID and store it in the database
        Args:
            user_id (str): User ID
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_data = {
            "user_id": user_id,
            "session_id": session_id
        }
        user_session = UserSession(**session_data)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve the user ID associated with a session ID from the database
        Args:
            session_id (str): Session ID
        Return:
            User ID or None if session_id is None or invalid
        """
        user_id = UserSession.search({"session_id": session_id})
        if user_id:
            return user_id
        return None

    def destroy_session(self, request=None):
        """
        Destroy a UserSession instance based on a Session ID from a request cookie
        Args:
            request: Request object containing the session cookie
        Return:
            True if session is destroyed, False otherwise
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_sessions = UserSession.search({"session_id": session_id})
        if user_sessions:
            user_sessions[0].remove()
            return True
        return False

