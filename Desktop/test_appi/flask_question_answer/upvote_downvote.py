from flask_question_answer.__init__ import db

user_upvote_question = db.Table('user_upvote_question', 
                                db.Column('user_id', db.String(50), db.ForeignKey('user.user_id')),
                                db.Column('question_id', db.String(50), db.ForeignKey('question.question_id')))

user_downvote_question = db.Table('user_downvote_question',
                                db.Column('user_id', db.String(50), db.ForeignKey('user.user_id')),
                                db.Column('question_id', db.String(50), db.ForeignKey('question.question_id')))
                                
user_upvote_answer = db.Table('user_upvote_answer',
                                db.Column('user_id', db.String(50), db.ForeignKey('user.user_id')),
                                db.Column('answer_id', db.String(50), db.ForeignKey('answer.answer_id')))


user_downvote_answer = db.Table('user_downvote_answer',
                                db.Column('user_id', db.String(50), db.ForeignKey('user.user_id')),
                                db.Column('answer_id', db.String(50), db.ForeignKey('answer.answer_id')))