#!/usr/bin/env python3
"""
Module for API authentication
"""

from flask import request
from typing import List, TypeVar
from os import getenv


class Authentication:
    """ Handles authentication """

    def requires_authentication(self, path: str, excluded_paths: List[str]) -> bool:
        """ Determines if API routes need authentication """
        if path is None or not excluded_paths:
            return True
        for excluded_path in excluded_paths:
            if excluded_path.endswith('*') and path.startswith(excluded_path[:-1]):
                return False
            elif excluded_path in {path, path + '/'}:
                return False
        return True

    def get_authorization_header(self, request=None) -> str:
        """ Checks for the presence and validity of the Authorization request header """
        if request is None or "Authorization" not in request.headers:
            return None
        else:
            return request.headers.get('Authorization')

    def get_current_user(self, request=None) -> TypeVar('User'):
        """ Returns the current user (placeholder) """
        return None

    def get_session_cookie(self, request=None):
        """ Retrieves the cookie value from a request """
        if request is None:
            return None

        return request.cookies.get(getenv('SESSION_NAME'))