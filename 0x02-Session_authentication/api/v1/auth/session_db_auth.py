#!/usr/bin/env python3
"""
Module for managing API sessions in a database
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from os import getenv

class SessionDBAuth(SessionExpAuth):
    """ Class for handling user sessions in a database """

    def create_session(self, user_id: str = None) -> str:
        """ Generates a unique Session ID for the specified user_id """
        if user_id is None or not isinstance(user_id, str):
            return None
        
        session_id = super().create_session(user_id)  # Call parent class method
        if session_id is None:
            return None

        SessionDBAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Retrieves the associated User ID based on the given Session ID """

        if session_id is None or not isinstance(session_id, str):
            return None
        else:
            return SessionDBAuth.user_id_by_session_id.get(session_id)

    def destroy_session(self, request=None):
        """ Deletes a user's session to initiate logout """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if user_id:
            del SessionDBAuth.user_id_by_session_id[session_id]
            super().destroy_session(request)  # Call parent class method
            return True
        
        return False