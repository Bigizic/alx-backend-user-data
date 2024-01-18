#!/usr/bin/env python3
"""New Flask view that handles all routes for the Session Authy
"""

from api.v1.views import app_views
from flask import request, jsonify
from models.user import User
from os import environ
from typing import Tuple


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def auth_session_login():
    """Implementation
    """
    email = request.form.get('email')

    if email is None or len(email.strip()) == 0:
        return jsonify({'error': "email missing"}), 401

    pwd = request.form.get('password')
    if pwd is None or len(pwd.strip()) == 0:
        return jsonfiy({'error': "password missing"}), 400

    user = User()
    data = user.search({'email': email})

    if len(data) <= 0:
        return jsonify({'error': "no user found for this email"}), 404

    if data:
        ps = data[0].is_valid_password(pwd)
        if ps:
            from api.v1.app import auth
            user_s = auth.create_session(getattr(data[0], 'id'))
            res = jsonify(data[0].to_json())
            res.set_cookie(environ.get('SESSION_NAME'), user_s)
            return res
        return jsonify({'error': "wrong password"}), 401
    return jsonify({'error': "no user found for this email"}), 404
