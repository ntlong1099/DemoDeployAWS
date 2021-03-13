from flask_question_answer.__init__ import app, db, jsonify, ma, request
from flask_question_answer.models import User, Question, Answer
from flask_question_answer.schema import answer_schema, answers_schema
from flask_question_answer.schema import question_schema, questions_schema
from flask_question_answer.schema import user_schema, users_schema
from flask_question_answer.upvote_downvote import user_upvote_question, user_downvote_question
from flask_question_answer.upvote_downvote import user_upvote_answer, user_downvote_answer

@app.route('/')
def home():
    return "TestHome_NguyenThanhLong_BE"

# Register
@app.route('/api/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']
    fullname = request.json['fullname']

    new_user = User(username, password, fullname)

    try:
        db.session.add(new_user)
        db.session.commit()
    except:
        return 'Username đã tồn tại!!!'

    return user_schema.jsonify(new_user)


# Login
@app.route('/api/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    user = User.query.filter_by(user_name=username).first()

    if not user:
        return "Tài khoản chưa được đăng ký!!!"

    if user.is_deleted:
        return 'Tài khoản đã bị xoá!!!'

    if user.user_password == password:
        return user_schema.jsonify(user)

    return 'Sai mật khẩu!!!'


# Delete user
@app.route('/api/user/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)

    user.delete()
    try:
        db.session.commit()
    except:
        return 'Error!!!123'

    return 'Tài khoản đã được xoá!!!'

# Get all question
@app.route('/api/question/all', methods=['GET'])
def get_all_questions():
    questions = Question.query.filter_by(is_deleted=False)
    result = questions_schema.dump(questions)

    return jsonify(result)

# Create 1 question
@app.route('/api/question', methods=['POST'])
def create_question():
    user_id = request.json['user_id']
    question_content = request.json['question_content']

    user = User.query.filter_by(user_id=user_id).first()

    if not user:
        return 'Tài khoản chưa được đăng ký!!!'

    question = Question(question_content, user_id)
    try:
        db.session.add(question)
        db.session.commit()
    except:
        return 'Câu hỏi đã tồn tại!!!'

    return question_schema.jsonify(question)


# Get question by id
@app.route('/api/question/<id>', methods=['GET'])
def get_question(id):
    question = Question.query.get(id)

    if not question:
        return 'Câu hỏi này không tồn tại!'

    if question.is_deleted:
        return 'Câu hỏi này đã bị xoá!'

    return question_schema.jsonify(question)


# Edit question by id
@app.route('/api/question/<id>', methods=['PUT'])
def edit_question(id):
    question_content = request.json['question_content']
    user_id = request.json['user_id']

    question = Question.query.get(id)

    if question.user_id != user_id:
        return 'Câu hỏi phải được sửa từ người tạo!!!'

    if not question:
        return 'Câu hỏi không tồn tại!!!'

    if question.is_deleted:
        return 'Câu hỏi đã bị xoá!!!'

    if question.is_closed:
        return 'Câu hỏi đã bị đóng!!!'

    question.edit(question_content)
    try:
        db.session.commit()
    except:
        return 'Lỗi cập nhập!!! PERMISSION'
    
    return question_schema.jsonify(question)


# Close question
@app.route('/api/question/<id>/close', methods=['DELETE'])
def close_question(id):
    user_id = request.json['user_id']

    question = Question.query.get(id)

    if not question:
        return 'Câu hỏi không tồn tại!!!'

    if question.user_id != user_id:
        return 'Câu hỏi phải đóng bởi người tạo!!!'

    question.close()
    try:
        db.session.commit()
    except:
        return 'Error permission!!!'

    return 'Câu hỏi đã đóng!!!'

# Delete question
@app.route('/api/question/<id>', methods=['DELETE'])
def delete_question(id):
    user_id = request.json['user_id']

    question = Question.query.get(id)

    if not question:
        return 'Câu hỏi không tồn tại!!!'

    if question.is_deleted:
        return 'Câu hỏi đã được xoá!!!'

    if question.user_id != user_id:
        return 'Câu hỏi phải được xoá bởi người tạo!!!'

    question.delete()
    try:
        db.session.commit()
    except:
        return 'Error!!!123'

    return 'Câu hỏi đã được xoá!!!'


# Create answer
@app.route('/api/question/<id>/answer', methods=['POST'])
def create_answer(id):
    user_id = request.json['user_id']
    answer_content = request.json['answer_content']

    user = User.query.filter_by(user_id=user_id).first()
    question = Question.query.get(id)

    if not question:
        return 'Câu hỏi không tồn tại!!'

    if question.is_deleted:
        return 'Câu hỏi đã bị xoá!!'

    if question.is_closed:
        return 'Câu hỏi đã bị đóng!!'

    if not user:
        return 'Tài khoản không tồn tại!!'

    answer = Answer(answer_content, user_id, id)

    try:
        db.session.add(answer)
        db.session.commit()
    except:
        return 'Error create answer!!!'

    return answer_schema.jsonify(answer)

# Get answer
@app.route('/api/answer/<id>', methods=['GET'])
def get_answer(id):
    answer = Answer.query.get(id)

    return answer_schema.jsonify(answer)

# Get all answers for question
@app.route('/api/question/<id>/answers', methods=['GET'])
def get_all_answers(id):
    question = Question.query.get(id)

    answer = Answer.query.filter_by(question_id=id, is_deleted=False)
    result = answers_schema.dump(answer)

    return jsonify(result)

# Edit answer
@app.route('/api/answer/<id>', methods=['PUT'])
def edit_answer(id):
    answer_content = request.json['answer_content']
    user_id = request.json['user_id']

    answer = Answer.query.get(id)

    if answer.user_id != user_id:
        return 'Câu trả lời chỉ được sửa bởi người tạo!!!'

    answer.edit(answer_content)
    try:
        db.session.commit()
    except:
        return 'Error edit answer!!!'

    return answer_schema.jsonify(answer)


# Delete answer
@app.route('/answer/<id>', methods=['DELETE'])
def delete_answer(id):
    user_id = request.json['user_id']

    answer = Answer.query.get(id)

    if answer.user_id != user_id:
        return 'Câu trả lời chỉ được xoá bởi người tạo!!!'

    answer.delete()
    try:
        db.session.commit()
    except:
        return 'Error delete answer!!!'

    return 'Xoá thành công!!!'

# Up vote of the question
@app.route('/api/question/<id>/upvote', methods=['PUT'])
def upvote_question(id):
    user_id = request.json['user_id']

    user = User.query.get(user_id)
    question = Question.query.get(id)

    upvote_user = question.upvote_user.all()
    downvote_user = question.downvote_user.all()

    if not question:
        return 'Câu hỏi không tồn tại!!!'
    
    if not user:
        return 'Tài khoản không tồn tại!!!'

    try:
        if user in upvote_user:
            question.dis_vote_up()
            question.upvote_user.remove(user)
        else:
            question.vote_up()
            question.upvote_user.append(user)
            if user in downvote_user:
                question.dis_vote_down()
                question.downvote_user.remove(user)
        
        db.session.commit()
    except:
        return 'Error!!'

    return question_schema.jsonify(question)

# Downvote of the question
@app.route('/api/question/<id>/downvote', methods=['PUT'])
def downvote_question(id):
    user_id = request.json['user_id']

    user = User.query.get(user_id)
    question = Question.query.get(id)

    upvote_user = question.upvote_user.all()
    downvote_user = question.downvote_user.all()

    if not question:
        return 'Câu hỏi không tồn tại!!!'
    
    if not user:
        return 'Tài khoản không tồn tại!!!'

    try:
        if user in downvote_user:
            question.dis_vote_down()
            question.downvote_user.remove(user)
        else:
            question.vote_down()
            question.downvote_user.append(user)
            if user in upvote_user:
                question.dis_vote_up()
                question.downvote_user.remove(user)
        
        db.session.commit()
    except:
        return 'Error!!'

    return question_schema.jsonify(question)

# Upvote of the answer
@app.route('/api/answer/<id>/upvote', methods=['PUT'])
def upvote_answer(id):
    user_id = request.json['user_id']

    user = User.query.get(user_id)
    answer = Answer.query.get(id)

    upvote_user = answer.upvote_user.all()
    downvote_user = answer.downvote_user.all()

    if not answer:
        return 'Câu trả lời không tồn tại!!!'
    
    if not user:
        return 'Tài khoản không tồn tại!!!'
    
    try:
        if user in upvote_user:
            answer.dis_vote_up()
            answer.upvote_user.remove(user)
        else:
            answer.vote_up()
            answer.upvote_user.append(user)
            if user in downvote_user:
                answer.dis_vote_down()
                answer.downvote_user.remove(user)
        
        db.session.commit()
    except:
        return 'Error!!'
    
    return answer_schema.jsonify(answer)

# Downvote of the answer
@app.route('/api/answer/<id>/downvote', methods=['PUT'])
def downvote_answer(id):
    user_id = request.json['user_id']

    user = User.query.get(user_id)
    answer = Answer.query.get(id)

    upvote_user = answer.upvote_user.all()
    downvote_user = answer.downvote_user.all()

    if not answer:
        return 'Câu trả lời không tồn tại!!!'
    
    if not user:
        return 'Tài khoản không tồn tại!!!'
    
    try:
        if user in downvote_user:
            answer.dis_vote_down()
            answer.downvote_user.remove(user)
        else:
            answer.vote_down()
            answer.downvote_user.append(user)
            if user in upvote_user:
                answer.dis_vote_up()
                answer.upvote_user.remove(user)
        
        db.session.commit()
    except:
        return 'Error!!'
    
    return answer_schema.jsonify(answer)


if __name__ == "__main__":
    db.create_all()
    # app.run(debug=True, host='0.0.0.0')
    app.run(debug=True)
