#!/usr/bin/env python3
""" Session authentication module a subclass of Auth
"""

from .auth import Auth
from flask import session, current_app
import logging
from models.user import User
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
        self.user_id_by_session_id[s_id] = user_id
        return s_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return:
            - user ID based on a session Id
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Return:
            - a User instance based on a cookie value
        """
        if request:
            req = self.session_cookie(request)
            return User.get(self.user_id_for_session_id(str(req)))
        return None

    def destroy_session(self, request=None) -> bool:
        """deletes the user session/logout
        """
        if request is None:
            return False
        re = self.session_cookie(request)
        if not re:
            return False
        user_id = self.user_id_for_session_id(re)
        if not user_id:
            return False
        # if user_id in self.user_id_by_session_id.values():
        del self.user_id_by_session_id[re]
        return True
