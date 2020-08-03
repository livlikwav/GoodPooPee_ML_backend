from flask import request
from flask_restful import Resource
from app.models.pet import Pet
from app import db, ma

class PetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pet

# make instances of schemas
pet_schema = PetSchema()
pets_schema = PetSchema(many=True)

class PetRegisterApi(Resource):
    def post(self):
        new_pet = Pet(
            name = request.json['name'],
            breed = request.json['breed'],
            gender = request.json['gender'],
            birth = request.json['birth'],
            adoption = request.json['adoption'],
            #user_id is not nullable
            user_id = request.json['user_id']
        )
        db.session.add(new_pet)
        db.session.commit()
        return pet_schema.dump(new_pet)


class PetApi(Resource):
    def get(self, pet_id):
        selected_pet = Pet.query.filter_by(id = pet_id).first()
        return pet_schema.dump(selected_pet)

    def put(self, pet_id):
        updated_pet = Pet.query.filter_by(id = pet_id).first()
        updated_pet.name = request.json['name']
        updated_pet.breed = request.json['breed']
        updated_pet.gender = request.json['gender']
        updated_pet.birth = request.json['birth']
        updated_pet.adoption = request.json['adoption']
        db.session.commit()
        return pet_schema.dump(updated_pet)

    def delete(self, pet_id):
        deleted_pet = Pet.query.filter_by(id = pet_id).first()
        db.session.delete(deleted_pet)
        db.session.commit()
        return '', 204