#!/usr/bin/env python3
"""
Main file
"""
from db import DB
from user import User

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


my_db = DB()

email = 'test@test.com'
hashed_password = "hashedPwd"
ema = "ola@gmail"
pwd = "run"

user = my_db.add_user(email, hashed_password)
ur = my_db.add_user(ema, pwd)
print(user.id)
print("-----------")
print(ur.id)
print(ur.hashed_password)

try:
    my_db.update_user(user.id, hashed_password='NewPwd')
    print("Password updated")
except ValueError:
    print("Error")

try:
    my_db.update_user(ur.id, age=3,  hashed_password="goat", session_id="something")
    print(ur.hashed_password, ur.session_id)
    print("password changed")
except ValueError:
    print("Error")
