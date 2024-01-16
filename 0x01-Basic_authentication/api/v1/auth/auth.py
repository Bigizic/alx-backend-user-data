#!/usr/bin/env python3
"""Auth class
- a class to manage the API authentication
"""

from typing import List, TypeVar
from flask import request


class Auth():
    """Auth class
    This class is the template for all authentication system
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Return:
            - False - path and excluded_paths
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path not in excluded_paths:
            return True

        new_path = path[-1]
        if new_path != '/':
            new_path = path + '/'
        else:
            new_path = path

        if new_path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Return:
            - None - request (will be the Flask request object)
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Return:
            - None - request (will be the Flask request object)
        """
        return None
