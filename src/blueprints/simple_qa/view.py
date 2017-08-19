from flask import Blueprint, jsonify, request
from flask_restful import Resource, Api, reqparse
from pony import orm
from .model import Question, Answer, User, Tag, Status, db
from src.common.database_helpers import recursive_to_dict


simp_qa = Blueprint('simple_qa', __name__,)
api = Api(simp_qa)

def easy_dict(data, show_hidden=False, show_related=True):
    local_kwargs = {}
    if show_hidden:
        local_kwargs.update({'with_lazy': True, 'with_collections': True})
    if show_related:
        local_kwargs.update({'related_objects': True})
    return recursive_to_dict(data, **local_kwargs)

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
        parser = reqparse.RequestParser()
        parser.add_argument('statusid', help='Need int(statusid)',
                            location='json', required=True)
        parser.add_argument('userid', help='Need int(userid)',
                            location='json',
                            required=True)
        parser.add_argument('title', help='Need str(title)', location='json',
                            required=True)
        parser.add_argument('question', help='Need str(question)',
                            location='json', required=True)
        args = parser.parse_args()


        statusid = Status[args['statusid']]
        userid = User[args['userid']]
        q = Question(statusid=statusid,
                     userid=userid,
                     title=args['title'],
                     question=args['question'])
        orm.commit()

        # TODO: return statements
        return {'You put in': args}

    def put(self):
        return {'a': 'put'}

    def delete(self):
        return {'Zoop': 'Zoop'}

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

class TagResource(Resource):

    @orm.db_session()
    def get(self, id=None):
        if id:
            data = [easy_dict(Tag[id], True)]
        else:
            dataset = orm.select(quest for quest in Tag)
            data = [easy_dict(i, True) for i in dataset]
        return jsonify({"results": data})

class JustATest(Resource):
    def get(self, id=None, other=None):
        print("JustATest")
        print(id)
        print(other)



api.add_resource(QuestionResource, '/question/', '/question/<int:id>')
api.add_resource(AnswerResource, '/answer/', '/answer/<int:id>')
api.add_resource(StatusResource, '/status/', '/status/<int:id>')
api.add_resource(UserResource, '/user/', '/user/<int:id>')
api.add_resource(TagResource, '/tag/', '/tag/<int:id>')
api.add_resource(JustATest, '/question/<int:id>/tester1',
                 '/question/<int:id>/tester2')






# s = Status(Name="Example")
# u = User(username='Kamori', email='example@example.com')
# @orm.db_session(serializable=True)
# def _post(self):
#     #print(db.check_tables())
#     #print(db.schema)
#     #print(dir(db))
#     #print(dir(Status))
#     s = Status(Name="Example")
#     u = User(username='Kamori', email='example@exmaple.com')
#     q = Question(statusid=s, userid=u, title='What is the answer',
#                  question='please give me the answer')
#     a = Answer(answer='here is the answer', questionid=q, userid=u,
#                statusid=s)
#     orm.commit()
#     resp = {}
#
#     dataset = orm.select(quest for quest in Question)
#     for res in dataset:
#         print('======== BEGIN ======')
#         recursive = (recursive_to_dict(res, with_collections=True,
#                                 related_objects=True))
#         print(recursive)
#         print('========  END  ======')
#         res = recursive
#         resp[res['id']] = res
#
#     dict_res = dataset.to_json(with_schema=True)
#     print('========  BEGIN FINAL  ======')
#     print(dict_res)
#     print('========   END FINAL   ======')
#     return jsonify(res)
#
#
#     # for res in orm.select(quest for quest in Question):
#     #     res = serialization.to_dict(res)
#     #     print(res)
#     #     resp['test'] = res
#     #     #res = res.to_dict(related_objects=True, with_collections=True)
#     #     #res =
#     #
#     #     #resp[res.id] = json.loads(res.to_json(with_schema=False))
#     #
#     # print(resp)
#     # return jsonify(resp)