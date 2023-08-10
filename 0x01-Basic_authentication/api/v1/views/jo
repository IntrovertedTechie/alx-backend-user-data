#!/usr/bin/env python3

"""
Module of Index views
"""

from flask import jsonify, abort
from api.v1.views import app_views

<<<<<<< HEAD

=======
>>>>>>> 60f5dfb25ac7d7825eb4d9abdf1ba3f728e59c41
@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ GET /api/v1/status
    Return:
       - the status of the API
    """
    return jsonify({"status": "OK"})

<<<<<<< HEAD

=======
>>>>>>> 60f5dfb25ac7d7825eb4d9abdf1ba3f728e59c41
@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized() -> str:
    """ GET /api/v1/unauthorized
    Return:
       - abort(401)
    """
    return abort(401)

<<<<<<< HEAD

=======
>>>>>>> 60f5dfb25ac7d7825eb4d9abdf1ba3f728e59c41
@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def forbidden() -> str:
    """ GET /api/v1/forbidden
    Return:
       - abort(403)
    """
    return abort(403)

<<<<<<< HEAD

=======
>>>>>>> 60f5dfb25ac7d7825eb4d9abdf1ba3f728e59c41
@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """ GET /api/v1/stats
    Return:
       - the number of each objects
    """
    stats = {}
    # Calculate and populate stats here, if needed
<<<<<<< HEAD
    return jsonify(stats)
=======
    return jsonify(stats)
>>>>>>> 60f5dfb25ac7d7825eb4d9abdf1ba3f728e59c41
