#!/usr/bin/env python3
"""A method that creates a password hash
"""

import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    """Implementation
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generates a UUID.
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Constructor
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Implementation
        """
        try:
            sm = self._db.find_user_by(email=str(email))
            if sm:
                raise ValueError(f"User {email} already exists")
        except NoResultFound as e:
            hashed_pwd = _hash_password(password)
            new_user = self._db.add_user(email, hashed_pwd)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates user password
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                tmp = user.hashed_password
                return bcrypt.checkpw(password.encode('utf-8'), tmp)
        except Exception as e:
            return False

    def create_session(self, email: str) -> str:
        """Creates a session
        Return:
            - Session id in uuid.uuid4() format
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                user.session_id = _generate_uuid()
                self._db.save()
                return user.session_id
        except Exception as e:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Finds user in db
        Return:
            - <user.User object> based on session_id
        """
        try:
            if session_id:
                user = self._db.find_user_by(session_id=session_id)
                return user if user else None
            return None
        except Exception as e:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Updates a user session id to None
        """
        try:
            user = self._db.find_user_by(id=user_id)
            if user:
                user.session_id = None
                self._db.save()
            return None
        except Exception as e:
            return None
