#!/usr/bin/env python3
"""
Definition of class Auth
"""
import base64
from typing import List, TypeVar
from api.v1.auth.session_auth import SessionAuth
from models.user import User

class Auth:
    """Auth class
    """
    def __init__(self):
        """ Initialize Auth instance
        """
        self.session_cookie_name = None
        if getenv('AUTH_TYPE') == 'session_auth':
            self.auth = SessionAuth()
            self.session_cookie_name = getenv('SESSION_NAME')

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if path requires authentication
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != '/':
            path += '/'
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Returns the value of the authorization header
        """
        if request is None or "Authorization" not in request.headers:
            return None
        return request.headers["Authorization"]

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the User instance for a request
        """
        if self.session_cookie_name and request:
            session_id = self.session_cookie(request)
            user_id = self.auth.user_id_for_session_id(session_id)
            return User.get(user_id)
        auth_header = self.authorization_header(request)
        if not auth_header:
            return None
        auth_credentials = self.extract_base64_authorization_header(auth_header)
        user_credentials = self.decode_base64_authorization_header(auth_credentials)
        user_email = user_credentials[0]
        user_pwd = user_credentials[1]
        user = User.search({'email': user_email})
        if not user or len(user) == 0:
            return None
        user = user[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def session_cookie(self, request=None) -> str:
        """Returns the value of the session cookie
        """
        if request is None or self.session_cookie_name not in request.cookies:
            return None
        return request.cookies[self.session_cookie_name]
