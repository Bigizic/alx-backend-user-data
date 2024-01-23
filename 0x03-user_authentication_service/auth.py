#!/usr/bin/env python3
"""A method that creates a password hash
"""

import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User

def _hash_password(password: str) -> bytes:
    """Implementation
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


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
            if self._db.find_user_by(email=email):
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            new_user = self._db.add_user(email, hashed_pwd)
            return new_user