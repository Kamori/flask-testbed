from flask import Flask, Blueprint
from src.blueprints.home_diagnostic.view import home_diagnostic
from src.blueprints.passwordmanager.view import pwm as password_manager
from src.blueprints.simple_qa.view import simp_qa as simple_qa

import os

def load_flask(settings, **kwargs):
    app = Flask(__name__)
    app.config.from_pyfile(settings)
    return app

def register_base_routes(app):

    @app.route('/')
    def index():
        return "Hello index page"

    @app.route('/testeroni')
    def testeroni():
        return "Still int he base app"

def register_blueprints(app):
    app.register_blueprint(home_diagnostic, url_prefix='/home')
    app.register_blueprint(password_manager, url_prefix='/passwd')
    app.register_blueprint(simple_qa, url_prefix='/simpleqa')


def configure():
    app = load_flask(settings='settings.py')

    register_base_routes(app)
    register_blueprints(app)


    return app