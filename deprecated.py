from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from datetime import datetime
import os

# generate Marshmallow schemas

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
pet_schema = PetSchema()
pets_schema = PetSchema(many=True)

# init flask-restful
api = Api(app)


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

