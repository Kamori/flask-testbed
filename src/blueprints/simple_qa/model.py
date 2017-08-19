from datetime import datetime
from pony.orm import *


db = Database()


class Question(db.Entity):
    _table_ = 'Questions'
    id = PrimaryKey(int, auto=True)
    userid = Required('User')
    title = Required(LongStr)
    question = Required(LongStr)
    statusid = Required('Status')
    tags = Set('Tag')
    answers = Set('Answer', reverse='questionid')
    bestanswer = Optional('Answer', nullable=True, reverse='bestof_question')
    created = Optional(datetime, sql_default="CURRENT_TIMESTAMP")
    updated = Optional(datetime, sql_default="CURRENT_TIMESTAMP")


class Answer(db.Entity):
    _table_ = 'Answers'
    id = PrimaryKey(int, auto=True)
    answer = Required(str)
    questionid = Required(Question, reverse='answers')
    statusid = Required('Status')
    userid = Required('User')
    bestof_question = Set(Question, reverse='bestanswer')
    created = Optional(datetime, sql_default="CURRENT_TIMESTAMP")
    updated = Optional(datetime, sql_default="CURRENT_TIMESTAMP")


class Status(db.Entity):
    _table_ = 'Statuses'
    id = PrimaryKey(int, auto=True)
    Name = Required(str, unique=True)
    questions = Set(Question)
    answers = Set(Answer)


class User(db.Entity):
    _table_ = 'Users'
    id = PrimaryKey(int, auto=True)
    username = Required(str, unique=True)
    email = Required(str, unique=True)
    questions = Set(Question)
    answers = Set(Answer)
    created = Optional(datetime, sql_default="CURRENT_TIMESTAMP")
    updated = Optional(datetime, sql_default="CURRENT_TIMESTAMP")


class Tag(db.Entity):
    _table_ = 'Tags'
    id = PrimaryKey(int, auto=True)
    questions = Set(Question)


sql_debug(True)
db.bind(provider='sqlite', filename=':memory:', create_db=True)
db.generate_mapping(create_tables=True)

# with db.set_perms_for(Question, Answer, Status, Tag):
#     perm('view', group='anybody')


