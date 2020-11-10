from flask import request
from flask_restful import Resource

from app import db
from app.models.user import User, UserSchema
from app.models.pet import Pet, PetSchema
from app.models.blacklist_user_token import BlacklistUserToken
from app.utils.decorators import confirm_account
from sqlalchemy.exc import IntegrityError

# make instances of schemas
user_schema = UserSchema()
pet_schema = PetSchema()

class RegisterApi(Resource):
    def post(self):
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
        # check user profile existency and password
        if login_user is not None and login_user.verify_password(user_pw):
            token = login_user.encode_auth_token(login_user.id)
            return {
                'access_token' : token.decode('UTF-8'),
                'user' : user_schema.dump(login_user),
                'pet' : pet_schema.dump(self.get_pet(login_user.id)),
            }, 200
        else:
            return {
                "msg" : "Fail to authentication"
            }, 401

    def get_pet(self, user_id: int) -> str:
        owned_pet = Pet.query.filter_by(user_id = user_id).first()
        if(owned_pet is not None):
            return owned_pet
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
