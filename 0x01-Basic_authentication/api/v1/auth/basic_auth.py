#!/usr/bin/env python3
"""A subclass of Auth
"""

import base64
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
        if auh is None or not isinstance(auh, str):
            return None
        if auh.split(' ')[0] == 'Basic' and auh.split(' ')[1]:
            return auh.split(' ')[1]
        return None

    def decode_base64_authorization_header(
                                           self,
                                           base64_authorization_header: str
                                           ) -> str:
        """
        Return:
            - decoded value of a Base64 string
        """
        data = base64_authorization_header
        if data is None or not isinstance(data, str):
            return None
        try:
            decode = base64.b64decode(data)
            if decode:
                return decode.decode('utf-8')
        except Exception as e:
            return None
