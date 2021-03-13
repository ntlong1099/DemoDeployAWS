database = db.sqlite

start api:
- python app.py

URI: 'localhost:5000'

Các API hiện có:
Register:
-POST       http://localhost:5000/api/register

Longin:
-POST       http://localhost:5000/api/login

Delete user by Id
-DELETE     http://localhost:5000/api/user/<id>

Get all question
-GET        http://localhost:5000/api/question/all

Create question
-POST       http://localhost:5000/api/question

Get question by Id
-GET        http://localhost:5000/api/question/<id>

Edit question by Id
-PUT        http://localhost:5000/api/question/<id>

Close question
-DELETE     http://localhost:5000/api/question/<id>/close

Delete question
-DELETE     http://localhost:5000/api/question/<id>

Create answer of the question
-POST       http://localhost:5000/api/question/<id>/answer

Get answer by Id
-GET        http://localhost:5000/api/answer/<id>

Get all answer of the question
-GET        http://localhost:5000/api/question/<id>/answers

Edit answer
-PUT        http://localhost:5000/api/answer/<id>

Delete answer
-DELETE     http://localhost:5000/answer/<id>

Upvote of the question
-PUT        http://localhost:5000/api/question/<id>/upvote

Downvote of the question
-PUT        http://localhost:5000/api/question/<id>/downvote

Upvote of the answer
-PUT        http://localhost:5000/api/answer/<id>/upvote

Downvote of the answer
-PUT        http://localhost:5000/api/answer/<id>/downvote
