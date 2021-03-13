from datetime import datetime
from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import os
import uuid

# Init app
app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))
# Data base
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(base_dir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
         
# Init database
db = SQLAlchemy(app)
# Init mallow
ma = Marshmallow(app)