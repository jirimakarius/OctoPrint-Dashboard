from functools import wraps
from flask import g, request
from octoprint_dashboard.services import LoginService
from octoprint_dashboard.model import User
from jwt import DecodeError, ExpiredSignature


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
        g.user = User.query.filter_by(username=payload['sub']).first()
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

        g.user = User.query.filter_by(username=payload['sub']).first()
        if g.user.superadmin is False:
            return 'You are not superadmin', 403

        return f(*args, **kwargs)
    return decorated_function
