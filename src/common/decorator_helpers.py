from flask import request
from functools import wraps

from src.common.safety_helpers import check_auth, must_authenticate


def requires_auth(secure_methods=None):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            method = request.method

            if not secure_methods or  method in secure_methods:
                auth = request.authorization

                if not auth or not check_auth(auth.username, auth.password):
                    return must_authenticate()

            return f(*args, **kwargs)

        return decorated

    return decorator
