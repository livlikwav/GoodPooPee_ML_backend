from flask import request, jsonify
from flask_restful import Resource
from app.models.pet import Pet
from app import db, ma
import datetime
class PetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pet
        include_fk = True

# make instances of schemas
pet_schema = PetSchema()
# pets_schema = PetSchema(many=True)

class PetRegisterApi(Resource):
    def post(self):
        # check that pet's name already exists
        pet = Pet.query.filter_by(user_id=request.json['user_id'], name=request.json['name']).first()
        if pet:
            return jsonify({
                "status" : "Fail",
                "msg" : f"name \'{pet.name}\' already exists"
            })
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
        # check that pet's name already exists
        pet = Pet.query.filter_by(user_id=request.json['user_id'], name=request.json['name']).first()
        if pet:
            return jsonify({
                "status" : "Fail",
                "msg" : f"name \'{pet.name}\' already exists"
            })
        updated_pet = Pet.query.filter_by(id = pet_id).first()
        updated_pet.name = request.json['name']
        updated_pet.breed = request.json['breed']
        updated_pet.gender = request.json['gender']
        updated_pet.birth = request.json['birth']
        updated_pet.adoption = request.json['adoption']
        updated_pet.last_modified_date = datetime.datetime.utcnow()
        db.session.commit()
        return pet_schema.dump(updated_pet)

    def delete(self, pet_id):
        from sqlalchemy.exc import IntegrityError
        deleted_pet = Pet.query.filter_by(id = pet_id).first()
        try:
            db.session.delete(deleted_pet)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({
                "status" : "Fail",
                "msg" : "IntegrityError of deleting pet profile, maybe because of foreign keys."
            })
        return jsonify({
            "status" : "Success",
            "msg" : "Successfully deleted pet profile."
        })
