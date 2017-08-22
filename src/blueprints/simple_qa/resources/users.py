from flask import jsonify
from flask_restful import Resource, Api, reqparse
from pony import orm
from ..model import Question, Answer, User, Tag, Status, db
from src.common.database_helpers import easy_dict
from src.common.response_codes import typeerror_response

class UserResource(Resource):

    @orm.db_session()
    def get(self, id=None):
        if id:
            data = [easy_dict(User[id], True)]
        else:
            dataset = orm.select(quest for quest in User)
            data = [easy_dict(i, True) for i in dataset]
        return jsonify({"results": data})

    @orm.db_session()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help='Need str(username)',
                            location='json', required=True)
        parser.add_argument('email', help='Need str(email)',
                            location='json',
                            required=True)
        args = parser.parse_args()


        User(username=args['username'], email=args['email'])
        orm.commit()

        # TODO: return statements
        return {'You put in': args}

    def put(self):
        return {'a': 'put'}

    def delete(self):
        return {'Zoop': 'Zoop'}