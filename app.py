from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_marshmallow import Marshmallow
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
# flask-marshmallow config
ma = Marshmallow(app)

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

    # pets = db.relationship('Pet', secondary=pets, lazy='subquery',
    #     backref=db.backref('users', lazy=True))
    # def __repr__(self):
    #     return f"<User : {self.id}, {self.email}, {self.first_name}, {self.last_name}>"

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

    records = db.relationship('PetRecord', backref='pet', lazy=True)

    users = db.relationship('User', secondary=UserPet, lazy='subquery',
        backref=db.backref('pets', lazy=True))
    # def __repr__(self):
    #     return f"<Pet : {self.id}, {self.name}, {self.breed}, {self.gender}, {self.birth}, {self.adoption}>"

class Ppcam(db.Model):
    __tablename__ = 'ppcam'
    id = db.Column(db.Integer, primary_key = True)
    serial_num = db.Column(db.String(250), nullable = False)
    created_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    last_modified_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    # def __repr__(self):
    #     return f"<Ppcam : {self.id}, {self.serial_num}>"

class Pad(db.Model):
    __tablename__ = 'pad'
    id = db.Column(db.Integer, primary_key = True)
    lu = db.Column(db.Integer, nullable = False)
    ld = db.Column(db.Integer, nullable = False)
    ru = db.Column(db.Integer, nullable = False)
    rd = db.Column(db.Integer, nullable = False)
    created_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    last_modified_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    # def __repr__(self):
    #     return f"<Pad : {self.id}, {self.iu}, {self.id}, {self.ru}, {self.rd}>"

# one-to-many relationships table
class PetRecord(db.Model):
    __tablename__ = 'pet_record'
    timestamp = db.Column(db.DateTime, primary_key = True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), primary_key = True)
    result = db.Column(db.String(250), nullable = False)
    photo_url = db.Column(db.String(250), nullable = False)
    created_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    last_modified_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    # def __repr__(self):
    #     return f"<Pet : {self.id}, {self.name}, {self.breed}, {self.gender}, {self.birth}, {self.adoption}>"

class DailyStatistics(db.Model):
    __tablename__ = 'daily_stat'
    timestamp = db.Column(db.DateTime, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), primary_key=True)
    count = db.Column(db.Integer, nullable = False)
    success = db.Column(db.Integer, nullable = False)
    fail = db.Column(db.Integer, nullable = False)

    # def __repr__(self):
    #     return f"<DailyStatistics : {self.count}, {self.success}, {self.fail}>"

class MonthlyStatistics(db.Model):
    __tablename__ = 'monthly_stat'
    timestamp = db.Column(db.DateTime, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), primary_key=True)
    count = db.Column(db.Integer, nullable = False)
    success = db.Column(db.Integer, nullable = False)
    progress = db.Column(db.Integer, nullable = False)

    # def __repr__(self):
    #     return f"<MonthlyStatistics : {self.count}, {self.success}, {self.progress}>"

db.create_all()

# generate Marshmallow schemas
class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
    
    id = ma.auto_field()
    email = ma.auto_field()
    first_name = ma.auto_field()
    last_name = ma.auto_field()
    password = ma.auto_field()
    created_date = ma.auto_field()
    last_modified_date = ma.auto_field()

class PetSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Pet
    
    id = ma.auto_field()
    name = ma.auto_field()
    breed = ma.auto_field()
    gender = ma.auto_field()
    birth = ma.auto_field()
    adoption = ma.auto_field()
    created_date = ma.auto_field()
    last_modified_date = ma.auto_field()

# make instances of schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)
pet_schema = PetSchema()
pets_schema = PetSchema(many=True)

# init flask-restful
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return jsonify(msg = 'Hello, world')

class UserResource(Resource):
    def post(self):
        new_user = User(
            # id = request.json['id'], < auto-increasing
            email = request.json['email'],
            first_name = request.json['first_name'],
            last_name = request.json['last_name'],
            password = request.json['password']
        )
        db.session.add(new_user)
        db.session.commit()
        return user_schema.dump(new_user)

class UserListResource(Resource):
    def get(self, user_id):
        selected_user = User.query.filter_by(id = user_id).first()
        return user_schema.dump(selected_user)

    def put(self, user_id):
        updated_user = User.query.filter_by(id = user_id).first()
        updated_user.email = request.json['email']
        updated_user.first_name = request.json['first_name']
        updated_user.last_name = request.json['last_name']
        updated_user.password = request.json['password']
        db.session.commit()
        return user_schema.dump(updated_user)

    def delete(self, user_id):
        deleted_user = User.query.filter_by(id = user_id)
        db.session.delete(deleted_user)
        db.session.commit()
        return '', 204

class UserPetResource(Resource):
    def get(self, user_id):
        # user_pets = db.session.query(UserPet).all()
        # for user_pet in user_pets:

        selected_pet = Pet.users.any(User.id == user_id)
        user_pet = db.session.query(UserPet).filter(selected_pet)

        pet = Pet.query.filter_by(id = user_id).first()
        # pet_id = user_pet.pet_id
        # selected_pet = Pet.query.filter_by(id = pet_id).first()
        return pet_schema.dump(user_pet)

class PetResource(Resource):
    def post(self):
        new_pet = Pet(
            name = request.json['name'],
            breed = request.json['breed'],
            gender = request.json['gender'],
            birth = request.json['birth'],
            adoption = request.json['adoption']
        )
        db.session.add(new_pet)
        db.session.commit()
        return pet_schema.dump(new_pet)

# Restful Routes
api.add_resource(HelloWorld, '/')
api.add_resource(UserResource, '/user')
api.add_resource(UserListResource, '/user/<int:user_id>')
api.add_resource(UserPetResource, '/user/<int:user_id>/pet')
api.add_resource(PetResource, '/pet')


# run server
# 0.0.0.0 to any host
if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')

# localhost = 127.0.0.1
# default port = 5000

