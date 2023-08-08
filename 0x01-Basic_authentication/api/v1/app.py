#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.auth import Auth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None

# Determine the authentication type based on the environment variable
if getenv("AUTH_TYPE") == 'basic_auth':
    auth = BasicAuth()  # Create an instance of BasicAuth for Basic Authentication
else:
    auth = Auth()  # Create an instance of Auth for other authentication types

@app.before_request
def request_filter() -> None:
    """ Pre-request filter to check if authorization is required
    """
    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/'
    ]

    if auth.require_auth(request.path, excluded_paths):
        if auth.authorization_header(request) is None:
            abort(401)  # Unauthorized if Authorization header is missing
        if auth.current_user(request) is None:
            abort(403)  # Forbidden if user authentication fails

@app.errorhandler(404)
def not_found(error) -> str:
    """ Error handler for 404 - Not Found
    """
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Error handler for 401 - Unauthorized
    """
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error) -> str:
    """ Error handler for 403 - Forbidden
    """
    return jsonify({"error": "Forbidden"}), 403

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
