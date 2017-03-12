from functools import wraps
from flask import g


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.get('user') is None:
            return "Párek"
        return f(*args, **kwargs)
    return decorated_function
