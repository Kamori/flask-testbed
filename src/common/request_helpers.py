from flask import request

def is_request(verb):
    if request.method == verb.upper():
        return True
    else:
        return False

def json_data(**kwargs):
    return request.get_json(**kwargs)