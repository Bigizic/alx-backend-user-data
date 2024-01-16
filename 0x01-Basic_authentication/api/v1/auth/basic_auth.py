#!/usr/bin/env python3
"""A subclass of Auth
"""

from api.v1.auth.auth import Auth
import base64
from flask import request
from models.user import User
from typing import TypeVar


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

    def extract_user_credentials(
                                 self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """Return:
            - user email and password from the Base64 decoded value
        """
        data = decoded_base64_authorization_header
        if data is None or not isinstance(data, str):
            return (None, None)

        data = str(data)

        if data.find(':') > 0:
            data = data.replace(':', ' ')
            return (data.split(' ')[0], data.split(' ')[1])
        return (None, None)

    def user_object_from_credentials(
                                     self,
                                     user_email: str,
                                     user_pwd: str
                                     ) -> TypeVar('User'):
        """Return
            - the User instance based on his email and password
        """
        e = isinstance(user_email, str)
        p = isinstance(user_pwd, str)
        if user_email is None or user_pwd is None or not e or not p:
            return None
        user_instance = User()
        try:
            data = user_instance.search({'email': user_email})
        except Exception:
            return None
        if len(data) <= 0:
            return None
        if data[0].is_valid_password(user_pwd):
            return data[0]
