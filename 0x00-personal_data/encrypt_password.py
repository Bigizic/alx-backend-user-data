#!/usr/bin/env python3
"""functions to encrypt passwords
"""

import bcrypt


def hash_password(password) -> str:
    """returns a salted bcrypt hash
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
