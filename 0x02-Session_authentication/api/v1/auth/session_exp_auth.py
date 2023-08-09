#!/usr/bin/env python3
"""
Module for managing API session expiration
"""

from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ Class for handling session expiration """

    def __init__(self):
        """ Initialize session duration """

        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """ Generates a unique Session ID for the specified user_id """

        try:
            session_id = super().create_session(user_id)
        except Exception:
            return None

        session_dictionary = self._create_session_dictionary(user_id)
        self.user_id_by_session_id[session_id] = session_dictionary

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Retrieves the associated User ID based on the given Session ID """

        if session_id is None or not isinstance(session_id, str):
            return None

        session_dict = self.user_id_by_session_id.get(session_id)

        if self._is_valid_session(session_dict):
            return session_dict.get('user_id')
        else:
            return None

    def _create_session_dictionary(self, user_id):
        """ Creates a dictionary for session information """
        return {
            'user_id': user_id,
            'created_at': datetime.now()
        }

    def _is_valid_session(self, session_dict):
        """ Checks if a session is valid """
        if session_dict is None or 'created_at' not in session_dict:
            return False

        if self.session_duration <= 0:
            return True

        created_time = session_dict.get('created_at')
        session_elapsed = timedelta(seconds=self.session_duration)

        return created_time + session_elapsed >= datetime.now()