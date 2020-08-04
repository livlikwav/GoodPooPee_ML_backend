from flask import request, jsonify
from flask_restful import Resource

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

class UserPetApi(Resource):
    def get(self, user_id):
        selected_user = User.query.filter_by(id = user_id).first()
        selected_pet = Pet.query.with_parent(selected_user).first()
        return pet_schema.dump(selected_pet)
