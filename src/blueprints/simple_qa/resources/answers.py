from flask import jsonify
from flask_restful import Resource, Api, reqparse
from pony import orm
from ..model import Question, Answer, User, Tag, Status, db
from src.common.database_helpers import easy_dict
from src.common.response_codes import typeerror_response

class AnswerResource(Resource):

    @orm.db_session()
    def get(self, id=None):
        if id:
            data = [easy_dict(Answer[id], True)]
        else:
            dataset = orm.select(quest for quest in Answer)
            data = [easy_dict(i, True) for i in dataset]
        return jsonify({"results": data})

    @orm.db_session()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('questionid', help='Need int(questionid)',
                            location='json', required=True)
        parser.add_argument('userid', help='Need int(userid)',
                            location='json',
                            required=True)
        parser.add_argument('statusid', help='Need int(statusid)',
                            location='json',
                            required=True)
        parser.add_argument('answer', help='Need str(answer)',
                            location='json', required=True)
        args = parser.parse_args()




        q = Question[args['questionid']]
        u = User[args['userid']]
        # TODO: do we need status on answer?
        s = Status[args['statusid']]
        a = Answer(answer=args['answer'], questionid=q, userid=u,
                   statusid=s)
        orm.commit()

        # TODO: return statements
        return {'You put in': args}

    def put(self):
        return {'a': 'put'}

    def delete(self):
        return {'Zoop': 'Zoop'}
