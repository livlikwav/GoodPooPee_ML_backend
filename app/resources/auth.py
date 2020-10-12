from flask import request, jsonify
from flask_restful import Resource
from flasgger import swag_from
import bcrypt

from app import db, ma
from app.models.user import User
from app.models.pet import Pet
from app.models.ppcam import Ppcam
from app.models.blacklist_user_token import BlacklistUserToken
from app.utils.decorators import confirm_account


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        
# make instances of schemas
user_schema = UserSchema()

class RegisterApi(Resource):
    def post(self):
        from sqlalchemy.exc import IntegrityError
        # check that email already exist
        exist_user = User.query.filter_by(email = request.json['email']).first()
        if(exist_user is not None):
            return {
                "msg" : "this email already exists"
            }, 409
        # create new user profile
        new_user = User(
            # id = request.json['id'], < auto-increasing
            email = request.json['email'],
            first_name = request.json['first_name'],
            last_name = request.json['last_name'],
            # automatically hash pw in User model
            password = request.json['password']
        )
        db.session.add(new_user)
        try: 
            db.session.commit()
        except IntegrityError:
            return {
                "msg" : "Fail to register user because of IntegrityError on db"
            }, 400
        return user_schema.dump(new_user)

class LoginApi(Resource):
    def post(self):
        # parsing request
        user_email = request.json['email']
        user_pw = request.json['password']
        # query related info of user
        login_user = User.query.filter_by(email = user_email).first()
        pet_id_of_user = self.get_pet_id(login_user.id)
        ppcam_id_of_user = self.get_ppcam_id(login_user.id)
        # check user profile existency and password
        if login_user is not None and login_user.verify_password(user_pw):
            token = login_user.encode_auth_token(login_user.id)
            return {
                'access_token' : token.decode('UTF-8'),
                'user_id' : login_user.id,
                'pet_id' : pet_id_of_user,
                'ppcam_id': ppcam_id_of_user
            }, 200
        else:
            return {
                "msg" : "Fail to authentication"
            }, 401

    def get_pet_id(self, user_id):
        owned_pet = Pet.query.filter_by(user_id = user_id).first()
        if(owned_pet is not None):
            return owned_pet.id
        else:
            return None
    
    def get_ppcam_id(self, user_id):
        owned_ppcam = Ppcam.query.filter_by(user_id = user_id).first()
        if(owned_ppcam is not None):
            return owned_ppcam.id
        else:
            return None

class LogoutApi(Resource):
    # Logout Resource
    @confirm_account
    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        # mark the token as blacklisted
        blacklist_token = BlacklistUserToken(token=auth_token)
        try:
            # insert the token
            db.session.add(blacklist_token)
            db.session.commit()
            return {
                'status' : 'Success',
                'message' : 'Successfully logged out.'
            }, 200
        except Exception as e:
            return {
                'status' : 'Fail',
                'message' : e
            }, 400
