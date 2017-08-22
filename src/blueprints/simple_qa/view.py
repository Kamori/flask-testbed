from flask import Blueprint, jsonify, request
from flask_restful import Api
from . import resources

simp_qa = Blueprint('simple_qa', __name__,)
api = Api(simp_qa)

# TODO: Make this auto magical
api.add_resource(resources.QuestionResource, '/question/',
                 '/question/<int:id>')
api.add_resource(resources.AnswerResource, '/answer/', '/answer/<int:id>')
api.add_resource(resources.StatusResource, '/status/', '/status/<int:id>')
api.add_resource(resources.UserResource, '/user/', '/user/<int:id>')
api.add_resource(resources.TagResource, '/tag/', '/tag/<int:id>')
