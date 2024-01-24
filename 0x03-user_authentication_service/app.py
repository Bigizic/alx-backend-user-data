#!/usr/bin/env python3
"""Basic Flask APP
"""

from auth import Auth
from flask import abort, Flask, jsonify, request

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
