from flask import Response


def check_auth(username, password):

    return username == 'admin' and password == 'secret'

def must_authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def safe_int(val, default=0):
    try:
        resp = int(val)
    except (TypeError, ValueError) as e:
        resp = default
    return resp