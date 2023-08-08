#!/usr/bin/env python3
"""
API authentication module
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """
     class
    """
    

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if API routes require authentication
        
        Args:
            path (str): The API route path
            excluded_paths (List[str]): List of excluded paths
        
        Returns:
            bool: True if authentication is required, False otherwise
        """
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True
        for i in excluded_paths:
            if i.endswith('/') and (path == i or path.startswith(i[:-1])):
                return False
        return True


    def authorization_header(self, request=None) -> str:
        """
        Checks if Authorization request header is present & contains values
        
        Args:
            request: Flask request object
        
        Returns:
            str: Authorization header value if present, otherwise None
        """
        if request is None or "Authorization" not in request.headers:
            return None
        else:
            return request.headers.get('Authorization')


    def current_user(self, request=None) -> TypeVar('User'):
        """
        Placeholder for current user information
        
        Args:
            request: Flask request object
        
        Returns:
            TypeVar('User'): Current user information or None
        """
        return None


def require_auth(self, path, excluded_paths):
    """ Determines if authentication is required for the given path """
    if path is None or not isinstance(path, str):
        return True

    if excluded_paths is None or not isinstance(excluded_paths, list):
        return True

    for excluded_path in excluded_paths:
        if excluded_path.endswith("*"):
            prefix = excluded_path.rstrip("*")
            if path.startswith(prefix):
                return False
        elif path == excluded_path:
            return False

    return True
