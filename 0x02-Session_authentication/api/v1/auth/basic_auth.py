#!/usr/bin/env python3
"""
Module for basic API authentication
"""

from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ Implements Basic Authentication """

    def extract_base64_from_authorization_header(
            self, authorization_header: str) -> str:
        """ Extracts the Base64 part of the Authorization header """
        if authorization_header and isinstance(
                authorization_header,
                str) and authorization_header.startswith("Basic "):
            return authorization_header[6:]

    def decode_base64(
            self, base64_value: str) -> str:
        """ Decodes a given Base64 value """
        if base64_value is None:
            return None
        if not isinstance(base64_value, str):
            return None

        try:
            return b64decode(base64_value).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64: str) -> (str, str):
        """ Extracts user email and password from decoded Base64 """
        if decoded_base64 is None:
            return None, None
        if not isinstance(decoded_base64, str):
            return None, None
        if ":" not in decoded_base64:
            return None, None
        email, pwd = decoded_base64.split(':', 1)
        return (email, pwd)

    def get_user_from_credentials(self,
                                  user_email: str,
                                  user_pwd: str) -> TypeVar('User'):
        """ Retrieves a User instance based on email and password """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
            return None

    def fetch_current_user(self, request=None) -> TypeVar('User'):
        """ Overrides Auth to fetch User instance for the request """

        # Get the authorization header from the request using Auth method
        auth_header = self.authorization_header(request)

        # Decode the authorization header value and retrieve user data using Basic Auth methods
        b64_header = self.extract_base64_from_authorization_header(auth_header)
        decoded_header = self.decode_base64(b64_header)
        user_creds = self.extract_user_credentials(decoded_header)
        return self.get_user_from_credentials(*user_creds)