#!/usr/bin/env python3
"""Auth class
- a class to manage the API authentication
"""

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
        return False

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