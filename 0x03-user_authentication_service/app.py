#!/usr/bin/env python3
"""Basic Flask APP
"""

from auth import Auth
from flask import abort, Flask, jsonify, redirect, request
from typing import Union

app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def basic_flask_app() -> jsonify:
    """Implementation
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=["POST"])
def register_user() -> jsonify:
    """Registers a user
    """
    email = request.form.get('email')
    pwd = request.form.get('password')

    try:
        registor = AUTH.register_user(email, pwd)
        return jsonify({'email': email, 'message': 'user created'})
    except ValueError as e:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=["POST"])
def login():
    """Handles user log in
    """
    email = request.form.get('email')
    pwd = request.form.get('password')

    validate_user = AUTH.valid_login(email, pwd)
    if validate_user:
        tmp = AUTH.create_session(email)
        data = jsonify({'email': email, 'message': 'logged in'})
        data.set_cookie('session_id', tmp)
        return data
    abort(401)


@app.route('/sessions', methods=["DELETE"], strict_slashes=False)
def logout():
    """Handles user log out
    """
    key = request.cookies.get('session_id')
    validate_user = AUTH.get_user_from_session_id(key)
    if validate_user:
        AUTH.destroy_session(validate_user.id)
        return redirect('/')
    abort(403)


@app.route('/profile', methods=["GET"], strict_slashes=False)
def user_profile() -> Union[jsonify, abort]:
    """Handles user profile
    Return:
        - <jsonify object> if user object exist
        - abort 403
    """
    key = request.cookies.get('session_id')
    validate_user = AUTH.get_user_from_session_id(key)
    if validate_user:
        return jsonify({'email': validate_user.email}), 200
    abort(403)


@app.route('/reset_password', methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """Resets user password
    """
    try:
        email = request.form.get('email')
        validate_user = AUTH.get_reset_password_token(email)
        if validate_user:
            return jsonify({'email': email, 'reset_token': validate_user})
        abort(403)
    except Exception as e:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
