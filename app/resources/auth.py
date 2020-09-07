from flask import request, jsonify
from flask_restful import Resource
from flasgger import swag_from
import bcrypt

from app import db, ma
from app.models.user import User
from app.models.blacklisttoken import BlacklistToken
from app.utils.decorators import confirm_account


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        
# make instances of schemas
user_schema = UserSchema()
# users_schema = UserSchema(many=True)

class RegisterApi(Resource):
    def post(self):
        from sqlalchemy.exc import IntegrityError
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
            return jsonify({
                "status" : "Fail",
                "msg" : "this email already exists"
            })
        return user_schema.dump(new_user)

class LoginApi(Resource):
    def post(self):
        user_email = request.json['email']
        user_pw = request.json['password']

        login_user = User.query.filter_by(email = user_email).first()
        if login_user is not None and login_user.verify_password(user_pw):
            token = login_user.encode_auth_token(login_user.id)
            return jsonify({
                'access_token' : token.decode('UTF-8')
            })
        else:
            return '', 401

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
        blacklist_token = BlacklistToken(token=auth_token)
        try:
            # insert the token
            db.session.add(blacklist_token)
            db.session.commit()
            return jsonify({
                'status' : 'Success',
                'message' : 'Successfully logged out.'
            })
        except Exception as e:
            return jsonify({
                'status' : 'Fail',
                'message' : e
            })
