from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_marshmallow import Marshmallow
from datetime import datetime
import os

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
        selected_pet = Pet.users.any(User.id == user_id)
        user_pet = db.session.query(UserPet).filter(selected_pet)
        pet = Pet.query.filter_by(id = user_id).first()
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

