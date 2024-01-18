#!/usr/bin/env python3
""" Session authentication module a subclass of Auth
"""

from api.v1.auth.auth import Auth
from flask import session
import uuid


class SessionAuth(Auth):
    """Implementation of subclass of Auth
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a Session ID for a user_id
        Return:
            - None if user_id is None
            - None if user_id is not str
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        s_id = str(uuid.uuid4())
        user_id_by_session[user_id] = s_id
        return s_id
