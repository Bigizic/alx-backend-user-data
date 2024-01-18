#!/usr/bin/env python3
""" authentication class subclass of SessionExpAuth
"""

from flask import request
from datetime import datetime, timedelta

from models.user_session import UserSession
from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """Implementation
    """

    def create_session(self, user_id=None) -> str:
        """Creates and stores a session id for the user
        """
        session_id = super().create_session(user_id)
        if isinstance(session_id, str):
            args = {
                'user_id': user_id,
                'session_id': session_id,
            }
            user_session = UserSession(**args)
            user_session.save()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieves the user id of the user associated with
        a given session id
        """
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None

        span = timedelta(seconds=self.session_duration)
        if (sessions[0].created_at + span) < datetime.now():
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None) -> bool:
        """Destroys an authenticated session.
        """
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False
        sessions[0].remove()
        return True
