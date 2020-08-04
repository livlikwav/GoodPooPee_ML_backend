from flask import request, jsonify
from flask_restful import Resource
from datetime import datetime, timedelta
import bcrypt
import jwt

from manage import app
from app import db, ma
from app.models.user import User
from app.models.pet import Pet

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class PetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pet

# make instances of schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)
pet_schema = PetSchema()
pets_schema = PetSchema(many=True)

class RegisterApi(Resource):
    def post(self):
        hash = bcrypt.hashpw(
            request.json['password'].encode('UTF-8'),
            bcrypt.gensalt()
        )
        new_user = User(
            # id = request.json['id'], < auto-increasing
            email = request.json['email'],
            first_name = request.json['first_name'],
            last_name = request.json['last_name'],
            hashed_password = hash
        )
        db.session.add(new_user)
        db.session.commit()
        return user_schema.dump(new_user)

class UserApi(Resource):
    def get(self, user_id):
        selected_user = User.query.filter_by(id = user_id).first()
        return user_schema.dump(selected_user)

    def put(self, user_id):
        updated_user = User.query.filter_by(id = user_id).first()
        updated_user.email = request.json['email']
        updated_user.first_name = request.json['first_name']
        updated_user.last_name = request.json['last_name']
        updated_user.hashed_password = request.json['password']
        db.session.commit()
        return user_schema.dump(updated_user)

    def delete(self, user_id):
        deleted_user = User.query.filter_by(id = user_id).first()
        db.session.delete(deleted_user)
        db.session.commit()
        return '', 204

class LoginApi(Resource):
    def post(self):
        user_email = request.json['email']
        user_pw = request.json['password']

        login_user = User.query.filter_by(email = user_email).first()
        if login_user is not None and login_user.verify_password(user_pw):
            encoded_jwt = jwt.encode({
                'user_id' : login_user.id,
                'exp' : datetime.utcnow() + timedelta(seconds = 60 * 60 * 24)
                },
                app.config['JWT_SECRET_KEY'],
                algorithm = 'HS256'
            )
            return jsonify({
                'access_token' : encoded_jwt.decode('UTF-8'),
                # 'DEBUG id' : login_user.id,
                # 'DEBUG exp' : (datetime.utcnow() + timedelta(seconds = 60 * 60 * 24)),
                # 'DEBUG key' : (app.config['JWT_SECRET_KEY'])
            })
        else:
            return '', 401

class UserPetApi(Resource):
    def get(self, user_id):
        selected_user = User.query.filter_by(id = user_id).first()
        selected_pet = Pet.query.with_parent(selected_user).first()
        return pet_schema.dump(selected_pet)
