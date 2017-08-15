from flask import Blueprint, render_template, request, make_response
from src.common.blueprint_helpers import bp_template_dir
from src.common.decorator_helpers import requires_auth
from src.common.request_helpers import is_request, json_data
from src.common.response_codes import empty_response
from .utils import online_status, set_online_status

home_diagnostic = Blueprint('hdiag', __name__,
                            template_folder=bp_template_dir('home_diagnostic'))

@home_diagnostic.route('/is-online', methods=['GET', 'PUT'])
@requires_auth(secure_methods=['PUT'])
def is_online():
    # Setup windows cron
    # Setup server backend
    # Add CSS and make it pretty
    if is_request('GET'):
        status, timestamp = online_status(True)
        resp = render_template('online_status.html',
                               status=status, timestamp=timestamp)
    elif is_request('PUT'):
        online = json_data(silent=True)
        if online:
            set_online_status(online.get('poll'))

        resp = empty_response(202, 'Uptime Submitted')

    return make_response(resp)
