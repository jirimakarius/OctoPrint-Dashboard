from flask import g
from flask_restful import marshal_with
from functools import wraps


def selective_marshal_with(fields, fields_private):
    """
    Selective response marshalling. Doesn't update apidoc.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            model = fields
            if g.user.superadmin:
                model.update(fields_private)
                print(model['temperature'])
            func2 = marshal_with(model)(func)
            return func2(*args, **kwargs)
        return wrapper
    return decorator

