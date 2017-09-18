from functools import wraps

from flask import g
from flask_restful import marshal_with


def selective_marshal_with(fields, fields_private):
    """
    Selective response marshalling.
    Adds specified fields to response if user has superadmin permission
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            model = fields
            if g.user.superadmin:
                model.update(fields_private)
            func2 = marshal_with(model)(func)
            return func2(*args, **kwargs)

        return wrapper

    return decorator
