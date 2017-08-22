from flask import jsonify
from flask_restful import Resource, Api, reqparse
from pony import orm
from ..model import Question, Answer, User, Tag, Status, db
from src.common.database_helpers import easy_dict
from src.common.response_codes import typeerror_response


class StatusResource(Resource):

    @orm.db_session()
    def get(self, id=None):
        if id:
            data = [easy_dict(Status[id], True)]
        else:
            dataset = orm.select(quest for quest in Status)
            data = [easy_dict(i, True) for i in dataset]
        return jsonify({"results": data})

    @orm.db_session()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', help='Need str(status_name)',
                            location='json', required=True)

        args = parser.parse_args()


        Status(Name=args['name'])
        orm.commit()

        # TODO: return statements
        return {'You put in': args}

    def put(self):
        return {'a': 'put'}

    def delete(self):
        return {'Zoop': 'Zoop'}