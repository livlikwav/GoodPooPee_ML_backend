from flask import request, jsonify
from flask_restful import Resource
from app.models.pet import Pet
from app.models.petrecord import PetRecord
from app import db, ma

import datetime

class PetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pet

class PetRecordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PetRecord

class RecordQuerySchema(ma.Schema):
    class Meta:
        fields = ["timestamp"]


# make instances of schemas
pet_schema = PetSchema()
# pets_schema = PetSchema(many=True)
pet_record_schema = PetRecordSchema()
# pet_records_schema = PetRecordSchema(many=True)
record_query_schema = RecordQuerySchema()

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
        updated_pet.last_modified_date = datetime.datetime.utcnow()
        db.session.commit()
        return pet_schema.dump(updated_pet)

    def delete(self, pet_id):
        deleted_pet = Pet.query.filter_by(id = pet_id).first()
        db.session.delete(deleted_pet)
        db.session.commit()
        return '', 204

class PetRecordApi(Resource):
    def post(self, pet_id):
        # find user by pet_id
        selected_pet = Pet.query.filter_by(id = pet_id).first()
        new_record = PetRecord(
            timestamp = request.json['timestamp'],
            result = request.json['result'],
            photo_url = request.json['photo_url'],
            pet_id = pet_id,
            user_id = selected_pet.user_id
        )
        if new_record:
            db.session.add(new_record)
            db.session.commit()
            return pet_record_schema.dump(new_record)
        else:
            return jsonify({
                "status" : "Fail",
                "msg" : new_record
            })

    def get(self, pet_id):
        # validate query string by ma
        errors = record_query_schema.validate(request.args)
        if errors:
            return jsonify({
                "status" : "fail",
                "msg" : "error in query schema validation"
            })
        # get timestamp in query string
        timestamp = request.args.get("timestamp")
        # get record by timestamp
        selected_record = PetRecord.query.filter_by(timestamp = timestamp).first()
        return pet_record_schema.dump(selected_record)


    def put(self, pet_id):
        # validate query string by ma
        errors = record_query_schema.validate(request.args)
        if errors:
            return jsonify({
                "status" : "fail",
                "msg" : "error in query schema validation"
            })
        # get timestamp in query string
        timestamp = request.args.get("timestamp")
        selected_record = PetRecord.query.filter_by(timestamp = timestamp).first()
        # update selected-record
        selected_record.timestamp = request.json['timestamp']
        selected_record.result = request.json['result']
        selected_record.photo_url = request.json['photo_url']
        selected_record.last_modified_date = datetime.datetime.utcnow()
        db.session.commit()
        return pet_record_schema.dump(selected_record)

    def delete(self, pet_id):
        # validate query string by ma
        errors = record_query_schema.validate(request.args)
        if errors:
            return jsonify({
                "status" : "fail",
                "msg" : "error in query schema validation"
            })
        # get timestamp in query string
        timestamp = request.args.get("timestamp")
        selected_record = PetRecord.query.filter_by(timestamp = timestamp).first()
        # delete selected-record
        db.session.delete(selected_record)
        db.session.commit()
        return jsonify({
            "status" : "success",
            "msg" : "successfully delete selected record"
        })

        