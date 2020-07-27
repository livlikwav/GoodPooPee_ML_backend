from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

# init app
app = Flask(__name__)
# app config by config.py
app.config.from_pyfile('config.py')
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DB_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# flask-sqlalchemy config
db = SQLAlchemy(app)

# init models = mapped classes
class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(250), nullable = False)
    first_name = db.Column(db.String(250), nullable = False)
    last_name = db.Column(db.String(250), nullable = False)
    password = db.Column(db.String(250), nullable = False)
    created_date = db.Column(db.DateTime, nullable = False)
    last_modified_date = db.Column(db.DateTime, nullable = False)

db.create_all()

@app.route('/', methods=['GET'])
def get():
    return jsonify(msg = 'Hello, world')

# run server
if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')

# localhost = 127.0.0.1
# default port = 5000

