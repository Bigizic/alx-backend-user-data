#!/usr/bin/env puython3
"""Basic Flask APP
"""

from auth import Auth
from flask import Flask, jsonify, request

app = Flask(__name__)
AUTH = AUTH()


@app.route('/', strict_slashes=False)
def basic_flask_app() -> str:
    """Implementation
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=["POST"])
def register_user():
    """Registers a user
    """
    email = request.form.get('email')
    pwd = request.form.get('password')

    try:
        registor = AUTH.register_user(email, pwd)
        return jsonify({'email': email, 'message': 'user created'})
    except ValueError as e:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
