from flask import jsonify
from flask_restful import Resource, Api, reqparse
from pony import orm
from ..model import Question, Answer, User, Tag, Status, db
from .tags import get_tags_by_name
from src.common.database_helpers import easy_dict
from src.common.response_codes import typeerror_response

class QuestionResource(Resource):

    @orm.db_session()
    def get(self, id=None):
        if id:
            data = [easy_dict(Question[id], True)]
        else:
            dataset = orm.select(quest for quest in Question)
            data = [easy_dict(i, True) for i in dataset]
        return jsonify({"results": data})

    @orm.db_session()
    def post(self):
        tags =  []
        parser = reqparse.RequestParser()
        parser.add_argument('statusid', type=int, help='Need int(statusid)',
                            location='json', required=True)
        parser.add_argument('userid', help='Need int(userid)',
                            location='json',
                            required=True)
        parser.add_argument('title', help='Need str(title)', location='json',
                            required=True)
        parser.add_argument('question', help='Need str(question)',
                            location='json', required=True)
        parser.add_argument('tags', action='append', location='json')
        args = parser.parse_args()

        if args.get('tags') and not isinstance(args['tags'], list):
            return typeerror_response('tags', args['tags'], list)
        elif args.get('tags'):
            tags = get_tags_by_name(args['tags'])


        statusid = Status[args['statusid']]
        userid = User[args['userid']]
        q = Question(statusid=statusid,
                     userid=userid,
                     title=args['title'],
                     question=args['question'],
                     tags=tags)
        orm.commit()

        # TODO: return statements
        return {'You put in': args}

    def put(self):
        return {'a': 'put'}

    def delete(self):
        return {'Zoop': 'Zoop'}