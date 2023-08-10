#!/usr/bin/env python3
"""
Definition of class Auth
"""
import os
from flask import request
from typing import (
    List,
    TypeVar
)
from api.v1.auth.session_auth import SessionAuth
from models.user import User

class Auth:
    """
    Manages the API authentication
    """
    def __init__(self):
        """
        Initializes Auth instance
        """
        self.auth = None
        if os.getenv('AUTH_TYPE') == 'session_auth':
            self.auth = SessionAuth()

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines whether a given path requires authentication or not
        Args:
            - path(str): Url path to be checked
            - excluded_paths(List of str): List of paths that do not require
              authentication
        Return:
            - True if path is not in excluded_paths, else False
        """
        if path is None:
            return True
        elif excluded_paths is None or excluded_paths == []:
            return True
        elif path in excluded_paths:
            return False
        else:
            for i in excluded_paths:
                if i.startswith(path):
                    return False
                if path.startswith(i):
                    return False
                if i[-1] == "*":
                    if path.startswith(i[:-1]):
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns the authorization header from a request object
        """
        if request is None:
            return None
        header = request.headers.get('Authorization')
        if header is None:
            return None
        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns a User instance from information from a request object
        """
        if self.auth and os.getenv('AUTH_TYPE') == 'session_auth':
            session_cookie = self.session_cookie(request)
            user_id = self.auth.user_id_for_session_id(session_cookie)
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

    def session_cookie(self, request=None):
        """
        Returns a cookie from a request
        Args:
            request : request object
        Return:
            value of _my_session_id cookie from request object
        """
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)