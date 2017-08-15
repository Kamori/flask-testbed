from flask import make_response
from src.common.exceptions import InvalidResponseCode
from src.common.mylocal import  locale

def empty_response(code=200, status=locale.production_log_search_phrase):
    if 200 > code > 300:
        raise InvalidResponseCode(f"Bad Status code 200-299 , Got: {code}")
    return make_response((status, code))