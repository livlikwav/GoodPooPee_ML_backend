from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
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

# create main Models/Tables
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(250), nullable = False)
    first_name = db.Column(db.String(250), nullable = False)
    last_name = db.Column(db.String(250), nullable = False)
    password = db.Column(db.String(250), nullable = False)
    created_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    last_modified_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f"<User : {self.id}, {self.email}, {self.first_name}, {self.last_name}>"

class Pet(db.Model):
    __tablename__ = 'pet'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(250), nullable = False)
    breed = db.Column(db.String(250), nullable = False)
    gender = db.Column(db.String(250), nullable = False)
    birth = db.Column(db.DateTime, nullable = False)
    adoption = db.Column(db.DateTime, nullable = False)
    created_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    last_modified_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    records = db.relationship('record', backref='pet', lazy=True)

    def __repr__(self):
        return f"<Pet : {self.id}, {self.name}, {self.breed}, {self.gender}, {self.birth}, {self.adoption}>"

class Ppcam(db.Model):
    __tablename__ = 'ppcam'
    id = db.Column(db.Integer, primary_key = True)
    serial_num = db.Column(db.String(250), nullable = False)
    created_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    last_modified_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f"<Ppcam : {self.id}, {self.serial_num}>"

class Pad(db.Model):
    __tablename__ = 'pad'
    id = db.Column(db.Integer, primary_key = True)
    lu = db.Column(db.Integer, nullable = False)
    ld = db.Column(db.Integer, nullable = False)
    ru = db.Column(db.Integer, nullable = False)
    rd = db.Column(db.Integer, nullable = False)
    created_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    last_modified_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f"<Pad : {self.id}, {self.iu}, {self.id}, {self.ru}, {self.rd}>"

# one-to-many relationships table
class PetRecord(db.Model):
    __tablename__ = 'pet_record'
    timestamp = db.Column(db.DateTime, primary_key = True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), primary_key = True)
    result = db.Column(db.String(250), nullable = False)
    photo_url = db.Column(db.String(250), nullable = False)
    created_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    last_modified_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f"<Pet : {self.id}, {self.name}, {self.breed}, {self.gender}, {self.birth}, {self.adoption}>"

class DailyStatistics(db.Model):
    __tablename__ = 'daily_stat'
    timestamp = db.Column(db.DateTime, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), primary_key=True)
    count = db.Column(db.Integer, nullable = False)
    success = db.Column(db.Integer, nullable = False)
    fail = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"<DailyStatistics : {self.count}, {self.success}, {self.fail}>"

class MonthlyStatistics(db.Model):
    __tablename__ = 'monthly_stat'
    timestamp = db.Column(db.DateTime, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), primary_key=True)
    count = db.Column(db.Integer, nullable = False)
    success = db.Column(db.Integer, nullable = False)
    progress = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"<MonthlyStatistics : {self.count}, {self.success}, {self.progress}>"

# many-to-many relationships helper table
# flask-sqlalchemy strongly recommend to not use a model but an actual table
UserPet = db.Table('user_pet',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('pet_id', db.Integer, db.ForeignKey('pet.id'), primary_key=True)
)

PpcamPad = db.Table('ppcam_pad',
    db.Column('ppcam_id', db.Integer, db.ForeignKey('ppcam.id'), primary_key=True),
    db.Column('pad_id', db.Integer, db.ForeignKey('pad.id'), primary_key=True)
)

UserPpcam = db.Table('user_ppcam',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('ppcam_id', db.Integer, db.ForeignKey('ppcam.id'), primary_key=True)
)

db.create_all()

@app.route('/', methods=['GET'])
def get():
    return jsonify(msg = 'Hello, world')

# run server
if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')

# localhost = 127.0.0.1
# default port = 5000

