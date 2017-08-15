from flask import Response, current_app


def check_auth(username, password):
    cnf = current_app.config
    return username == cnf['BASIC_AUTH_USER'] and password == cnf[
        'BASIC_AUTH_PASS']

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