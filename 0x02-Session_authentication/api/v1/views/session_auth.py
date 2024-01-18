#!/usr/bin/env python3
"""New Flask view that handles all routes for the Session Authy
"""

from api.v1.views import app_views
from flask import request, jsonify
from models.user import User
from os import environ
from typing import Tuple


@app_views.route('/auth_session/login', methods=['GET', 'POST'],
                 strict_slashes=False)
def auth_session_login() -> Tuple[str, int]:
    """Implementation
    """
    email = request.form.get('email')
    pwd = request.form.get('password')

    if email is None:
        return jsonify({'error': "email missing"}), 400
    if password is None:
        return jsonfiy({'error': "password missing"}), 400
    user = User()
    data = user.search({'email': email})
    if len(data) <= 0:
        return jsonify({'error': "no user found for this email"}), 404
    if data:
        ps = data[0].is_valid_password(pwd)
        if ps:
            from api.v1.app import auth
            user_s = auth.create_session(getattr(data[0], id))
            res = jsonify(data[0].to_json())
            res.set_cookie(environ.get('SESSION_NAME'), user_s)
            return res
        return jsonify({'error': "wrong_password"}), 401
    return jsonify({'error': "no user found for this email"}), 404