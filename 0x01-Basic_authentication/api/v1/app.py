#!/usr/bin/env python3
"""
Route module for the API
"""

from api.v1.auth.auth import Auth
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth_type = os.environ.get("AUTH_TYPE", None)
auth = None
if auth_type:
    from api.vi.auth.auth import Auth
    auth = Auth()


@app.before_request
def handler() -> None:
    """ Filters each request
    """
    global auth

    path = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']

    if auth is None:
        return

    if request.path not in path and auth.require_auth(request.path, path):
        if auth.authorization_header(request) is None:
            abort(401)
        if auth.current_user(request) is None:
            abort(403)


@app.errorhandler(401)
def request_unauthorized(error) -> str:
    """ request unauthorized eror
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def not_allowed(error) -> str:
    """ HTTP status code for a request where the user is
    authenticate but not allowed to access to a resource
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
