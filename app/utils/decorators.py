from functools import wraps

from flask import request
from flask_restplus import abort

from app.v1.core.UserService import verify_auth_token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        response = verify_auth_token(request.headers.get('Authorization'))
        if response.get("status") != "success":
            abort(401, message="Invalid or expired token, login again")

        return f(*args, **kwargs)

    return decorated


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        response = verify_auth_token(request.headers.get('Authorization'))
        data = response.get("data")
        if response.get("status") != "success":
            abort(401, message="Invalid or expired token, login again")

        admin = data.get("admin")
        if not admin:
            abort(401, message="Admin token required")

        return f(*args, **kwargs)

    return decorated
