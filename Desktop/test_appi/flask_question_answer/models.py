from flask_question_answer.__init__ import datetime, db, uuid
from flask_question_answer.upvote_downvote import user_upvote_question, user_downvote_question, user_downvote_answer, user_upvote_answer

class Question(db.Model):
    question_id = db.Column(db.String(50), primary_key=True)
    question_content = db.Column(db.Text, nullable=False, unique=True)
    upvote = db.Column(db.Integer, nullable=False)
    downvote = db.Column(db.Integer, nullable=False)
    date_create = db.Column(db.DateTime, nullable=False)
    date_update = db.Column(db.DateTime, nullable=False)
    is_closed = db.Column(db.Boolean, nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.String(50), db.ForeignKey(
        'user.user_id'), nullable=False)
    answers = db.relationship('Answer', backref='question', lazy=True)
    upvote_user = db.relationship('User', secondary=user_upvote_question, backref='upvote_questions', lazy='dynamic')
    downvote_user = db.relationship('User', secondary=user_downvote_question, backref='downvote_questions', lazy='dynamic')

    def __init__(self, content, user_id):
        self.question_id = uuid.uuid4().hex
        self.question_content = content
        self.user_id = user_id
        self.upvote = 0
        self.downvote = 0
        self.date_create = datetime.now()
        self.date_update = datetime.now()
        self.is_closed = False
        self.is_deleted = False

    def vote_up(self):
        self.upvote += 1

    def dis_vote_up(self):
        self.upvote -= 1

    def vote_down(self):
        self.downvote += 1

    def dis_vote_down(self):
        self.downvote -= 1

    def edit(self, content):
        self.question_content = content
        self.date_update = datetime.now()

    def delete(self):
        self.is_deleted = True

    def close(self):
        self.is_closed = True


# Answer Class/Model
class Answer(db.Model):
    answer_id = db.Column(db.String(50), primary_key=True)
    answer_content = db.Column(db.Text, nullable=False, unique=True)
    upvote = db.Column(db.Integer, nullable=False)
    downvote = db.Column(db.Integer, nullable=False)
    date_create = db.Column(db.DateTime, nullable=False)
    date_update = db.Column(db.DateTime, nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.String(50), db.ForeignKey(
        'user.user_id'), nullable=False)
    question_id = db.Column(db.String(50), db.ForeignKey(
        'question.question_id'), nullable=False)
    upvote_user = db.relationship('User', secondary=user_upvote_answer, backref='upvote_answer', lazy='dynamic')
    downvote_user = db.relationship('User', secondary=user_downvote_answer, backref='downvote_answer', lazy='dynamic')

    def __init__(self, content, user_id, question_id):
        self.answer_id = uuid.uuid4().hex
        self.answer_content = content
        self.user_id = user_id
        self.upvote = 0
        self.downvote = 0
        self.date_create = datetime.now()
        self.date_update = datetime.now()
        self.question_id = question_id
        self.is_deleted = False

    def vote_up(self):
        self.upvote += 1

    def dis_vote_up(self):
        self.upvote -= 1

    def vote_down(self):
        self.downvote += 1

    def dis_vote_down(self):
        self.downvote -= 1

    def edit(self, content):
        self.answer_content = content
        self.date_update = datetime.now()

    def delete(self):
        self.is_deleted = True

# User Class/Model
class User(db.Model):
    user_id = db.Column(db.String(50), primary_key=True)
    user_name = db.Column(db.String(20), nullable=False, unique=True)
    user_password = db.Column(db.String(18), nullable=False)
    user_fullname = db.Column(db.String(20), nullable=False)
    answers = db.relationship('Question', backref='owner', lazy=True)
    answers = db.relationship('Answer', backref='owner', lazy=True)
    is_deleted = db.Column(db.Boolean, nullable=False)

    def __init__(self, name, password, fullname):
        self.user_id = uuid.uuid4().hex
        self.user_name = name
        self.user_password = password
        self.user_fullname = fullname
        self.is_deleted = False

    def delete(self):
        self.is_deleted = True