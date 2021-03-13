from flask_question_answer.__init__ import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'user_name', 'user_email', 'user_password')


class QuestionSchema(ma.Schema):
    class Meta:
        fields = ('question_id', 'question_content', 'isclosed',
                  'up_vote', 'down_vote', 'date_public', 'user_id')

class AnswerSchema(ma.Schema):
    class Meta:
        fields = ('answer_id', 'answer_content', 'up_vote',
                  'down_vote', 'date_public', 'user_id', 'question_id')



user_schema = UserSchema()
users_schema = UserSchema(many=True)
question_schema = QuestionSchema()
questions_schema = QuestionSchema(many=True)
answer_schema = AnswerSchema()
answers_schema = AnswerSchema(many=True)
