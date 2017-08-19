from flask import make_response, jsonify, request
from src.common.exceptions import InvalidResponseCode
from src.common.mylocal import  locale

def empty_response(code=200, status=locale.production_log_search_phrase):
    if 200 > code > 300:
        raise InvalidResponseCode(f"Bad Status code 200-299, Got: {code}")
    return make_response((status, code))

def typeerror_response(field, value, expected_type, code=500):
    if 500 > code > 600:
        raise InvalidResponseCode(f"Bad Status code 500-599, Got: {code}")

    resp = {"field": field,
            "value": value,
            "expected": str(expected_type),
            "raw": str(request.get_data()),
            "msg": locale.response_typeerror_default.format(
                field=field,
                value=value,
                expected_type=expected_type)}
    return make_response((jsonify(resp), code))