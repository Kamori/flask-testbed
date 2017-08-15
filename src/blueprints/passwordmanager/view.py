from flask import Blueprint, render_template, request, make_response, \
    current_app
from src.common.blueprint_helpers import bp_template_dir
from src.common.decorator_helpers import requires_auth
import tpm

pwm = Blueprint('pwm', __name__,
                template_folder=bp_template_dir('passm'))

@pwm.route('/list')
@requires_auth()
def list_all():

    # Scrap this, TPM doesn't offer api access in their free version
    cnf = current_app.config
    mytpm = tpm.TpmApiv4(cnf['TPM_HOST'], username=cnf['TPM_USER'],
                         password=cnf['TPM_PASS'])

    print(mytpm.list_passwords())
    return "This is a response"
