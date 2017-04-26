from flask import g, request
from functools import wraps
from jwt import DecodeError, ExpiredSignature

from octoprint_dashboard.model import User
from octoprint_dashboard.services import LoginService


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.headers.get('Authorization'):
            return "Missing authorization header", 401

        try:
            payload = LoginService.parse_api_token(request)
        except DecodeError:
            return 'Token is invalid', 401
        except ExpiredSignature:
            return 'Token has expired', 401
        g.user = User.query.filter_by(username=payload['username']).first()
        return f(*args, **kwargs)

    return decorated_function


def superadmin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.headers.get('Authorization'):
            return "Missing authorization header", 401

        try:
            payload = LoginService.parse_api_token(request)
        except DecodeError:
            return 'Token is invalid', 401
        except ExpiredSignature:
            return 'Token has expired', 401

        g.user = User.query.filter_by(username=payload['username']).first()
        if g.user.superadmin is False:
            return 'You are not superadmin', 401

        return f(*args, **kwargs)

    return decorated_function
