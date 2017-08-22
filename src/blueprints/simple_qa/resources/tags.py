from flask import jsonify
from flask_restful import Resource, Api, reqparse
from pony import orm
from ..model import Question, Answer, User, Tag, Status, db
from src.common.database_helpers import easy_dict
from src.common.response_codes import typeerror_response

def get_tags_by_name(tags):
    """
    Converts a list/tuple of str tags to Tag objects, creates them if they
    don't exist
    :param tags: list(str, str, str)
    :return: list(Tag, Tag, Tag)
    """
    _tags = []
    for tag in tags:
        # Create the tag if it doesn't exist
        tag = Tag.get(name=tag) or Tag(name=tag)
        _tags.append(tag)
    return _tags


class TagResource(Resource):

    @orm.db_session()
    def get(self, id=None):
        if id:
            data = [easy_dict(Tag[id], True)]
        else:
            dataset = orm.select(quest for quest in Tag)
            data = [easy_dict(i, True) for i in dataset]
        return jsonify({"results": data})