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

        new_path = path[-1]
        if new_path != '/':
            new_path = path + '/'
        else:
            new_path = path

        new_exe_paths = []
        for items in excluded_paths:
            if items[-1] != '/':
                items += '/'
                new_exe_paths.append(items)
            else:
                new_exe_paths.append(items)

        if new_path in new_exe_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Return:
            - None - request (will be the Flask request object)
        """
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Return:
            - None - request (will be the Flask request object)
        """
        return None
