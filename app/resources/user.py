from flask import request
from flask_restful import Resource
import datetime

from app import db
from app.models.user import User, UserSchema
from app.models.pet import Pet, PetSchema
from app.models.ppcam import Ppcam, PpcamSchema
from app.utils.decorators import confirm_account

# make instances of schemas
user_schema = UserSchema()
pets_schema = PetSchema(many = True)
ppcams_schema = PpcamSchema(many = True)

class UserApi(Resource):
    @confirm_account
    def get(self, user_id):
        selected_user = User.query.filter_by(id = user_id).first()
        if(selected_user is None):
            return {
                "msg" : "User not found"
            }, 404
        return user_schema.dump(selected_user), 200

    @confirm_account
    def put(self, user_id):
        from sqlalchemy.exc import IntegrityError
        updated_user = User.query.filter_by(id = user_id).first()
        if(updated_user is None):
            return {
                "msg" : "User not found"
            }, 404
        try:
            updated_user.email = request.json['email']
            updated_user.first_name = request.json['first_name']
            updated_user.last_name = request.json['last_name']
            updated_user.last_modified_date = datetime.datetime.utcnow()
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return {
                "status" : "Fail",
                "msg" : "IntegrityError on updating user."
            }, 409
        return user_schema.dump(updated_user), 200

    @confirm_account
    def delete(self, user_id):
        from sqlalchemy.exc import IntegrityError
        deleted_user = User.query.filter_by(id = user_id).first()
        if(deleted_user is None):
            return {
                "msg" : "User not found"
            }, 404
        try:
            db.session.delete(deleted_user)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return {
                "status" : "Fail",
                "msg" : "IntegrityError on deleting user, maybe because of foreign keys."
            }, 409
        return {
            "status" : "Success",
            "msg" : "Successfully deleted user profile."
        }, 200

class UserPetApi(Resource):
    @confirm_account
    def get(self, user_id):
        selected_pets = Pet.query.filter_by(user_id=user_id).all()
        if(selected_pets is None):
            return {
                "msg" : "Pets not found"
            }, 404
        return pets_schema.dump(selected_pets), 200

class UserPpcamApi(Resource):
    @confirm_account
    def get(self, user_id):
        selected_ppcams = Ppcam.query.filter_by(user_id=user_id).all()
        if(selected_ppcams is None):
            return {
                "msg" : "Ppcams not found"
            }, 404
        return ppcams_schema.dump(selected_ppcams), 200