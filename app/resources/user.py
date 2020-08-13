from flask import request, jsonify
from flask_restful import Resource
import datetime

from app import db, ma
from app.models.user import User
from app.models.pet import Pet
from app.models.ppcam import Ppcam

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class PetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pet
        include_fk = True

class PpcamSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ppcam
        include_fk = True

# make instances of schemas
user_schema = UserSchema()
# users_schema = UserSchema(many=True)
pet_schema = PetSchema()
# pets_schema = PetSchema(many=True)
ppcam_schema = PpcamSchema()
# ppcams_schema = PpcamSchema(many=True)

class UserApi(Resource):
    def get(self, user_id):
        selected_user = User.query.filter_by(id = user_id).first()
        return user_schema.dump(selected_user)

    def put(self, user_id):
        from sqlalchemy.exc import IntegrityError
        updated_user = User.query.filter_by(id = user_id).first()
        try:
            updated_user.email = request.json['email']
            updated_user.first_name = request.json['first_name']
            updated_user.last_name = request.json['last_name']
            updated_user.last_modified_date = datetime.datetime.utcnow()
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({
                "status" : "Fail",
                "msg" : "IntegrityError on updating user."
            })
        return user_schema.dump(updated_user)

    def delete(self, user_id):
        from sqlalchemy.exc import IntegrityError
        deleted_user = User.query.filter_by(id = user_id).first()
        try:
            db.session.delete(deleted_user)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({
                "status" : "Fail",
                "msg" : "IntegrityError on deleting user, maybe because of foreign keys."
            })
        return jsonify({
            "status" : "Success",
            "msg" : "Successfully deleted user profile."
        })

class UserPetApi(Resource):
    def get(self, user_id):
        selected_user = User.query.filter_by(id = user_id).first()
        selected_pet = Pet.query.with_parent(selected_user).first()
        return pet_schema.dump(selected_pet)

class UserPpcamApi(Resource):
    def get(self, user_id):
        selected_user = User.query.filter_by(id = user_id).first()
        selected_ppcam = Ppcam.query.with_parent(selected_user).first()
        return ppcam_schema.dump(selected_ppcam)