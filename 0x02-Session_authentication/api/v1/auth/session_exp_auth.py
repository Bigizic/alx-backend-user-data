#!/usr/bin/env python3
"""A an expiration date to a Session ID subclass of SessionAuth
"""

from .session_auth import SessionAuth
from datetime import datetime, timedelta
from os import environ


class SessionExpAuth(SessionAuth):
    """Implementation
    """

    def __init__(self):
        """Constructor
        """
        super().__init__()
        duration = environ.get('SESSION_DURATION')
        if duration is None or not int(duration):
            self.session_duration = 0
        else:
            self.session_duration = int(duration)

    def create_session(self, user_id=None):
        """Implementation
        """
        ps = super().create_session(user_id)
        if not isinstance(ps, str):
            return None
        self.user_id_by_session_id[ps] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return ps

    def user_id_for_session_id(self, session_id=None):
        """Implementation
        """
        if session_id is None:
            return None
        ps = self.user_id_by_session_id.get(session_id)
        if ps is None or ps.get('created_at') is None:
            return None
        if self.session_duration <= 0:
            return ps.get('user_id')
        span = timedelta(seconds=self.session_duration)
        if (ps.get('created_at') + span) < datetime.now():
            return None
        return ps.get('user_id')
