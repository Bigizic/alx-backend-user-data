#!/usr/bin/env python3
"""A subclass of Auth
"""

from flask import request
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Implementation
    """

    def extract_base64_authorization_header(
                                            self,
                                            authorization_header: str
                                            ) -> str:
        """
        Return:
            - Base64 part of the Authorization header for a BasicAuthentication
        """
        auh = authorization_header
        if auth is None or not isinstance(auh, str):
            return None
        if auh.split(' ')[0] == 'Basic' and auh.split(' ')[1]:
            return auh.split(' ')[1]
        return None
