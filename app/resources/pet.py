from flask import request, jsonify
from flask_restful import Resource
from app.models.pet import Pet
from app.models.petrecord import PetRecord
from app import db, ma
import sys
import datetime
class PetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pet
        include_fk = True

class PetRecordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PetRecord
        include_fk = True

class RecordQuerySchema(ma.Schema):
    class Meta:
        fields = ["timestamp"]


# make instances of schemas
pet_schema = PetSchema()
# pets_schema = PetSchema(many=True)
pet_record_schema = PetRecordSchema()
deleted_record_schema = PetRecordSchema(only=("timestamp", "pet_id", "user_id"))
# pet_records_schema = PetRecordSchema(many=True)
record_query_schema = RecordQuerySchema()

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
        deleted_pet = Pet.query.filter_by(id = pet_id).first()
        db.session.delete(deleted_pet)
        db.session.commit()
        return '', 204

class PetRecordApi(Resource):
    def post(self, pet_id):
        from sqlalchemy.exc import IntegrityError
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
            try:
                db.session.commit()
            except IntegrityError as e:
                return jsonify({
                    "status" : "Fail",
                    "msg" : "IntegrityError on post new pet_record, check primary keys"
                })
            # update stat tables
            new_record.update_stats(request.json['timestamp'])
            return pet_record_schema.dump(new_record)
        else:
            return jsonify({
                "status" : "Fail",
                "msg" : "failed to make new pet record instance"
            })

    def get(self, pet_id):
        # validate query string by ma
        errors = record_query_schema.validate(request.args)
        if errors:
            return jsonify({
                "status" : "fail",
                "msg" : "error in get method - query schema validation"
            })
        # get timestamp in query string
        timestamp = request.args.get("timestamp")
        # get record by timestamp
        selected_record = PetRecord.query.filter_by(timestamp = timestamp).first()
        return pet_record_schema.dump(selected_record)


    def put(self, pet_id):
        from sqlalchemy.exc import IntegrityError
        # validate query string by ma
        errors = record_query_schema.validate(request.args)
        if errors:
            return jsonify({
                "status" : "fail",
                "msg" : "error in put method - query schema validation"
            })
        # get timestamp in query string
        last_timestamp = request.args.get("timestamp")
        # querying record
        selected_record = PetRecord.query.filter_by(timestamp = last_timestamp).first()
        # update selected-record
        try:
            selected_record.timestamp = request.json['timestamp']
            selected_record.result = request.json['result']
            selected_record.photo_url = request.json['photo_url']
            selected_record.last_modified_date = datetime.datetime.utcnow()
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({
                "status" : "Fail",
                "msg" : "Error in PetRecord, Put Api, check primary_keys"
            })
        # update stat tables
        selected_record.update_stats(last_timestamp)
        return pet_record_schema.dump(selected_record)

    def delete(self, pet_id):
        # validate query string by ma
        errors = record_query_schema.validate(request.args)
        if errors:
            return jsonify({
                "status" : "fail",
                "msg" : "error in delete method - query schema validation"
            })
        # get timestamp in query string
        last_timestamp = request.args.get("timestamp")
        selected_record = PetRecord.query.filter_by(timestamp = last_timestamp).first()
        db.session.delete(selected_record)
        db.session.commit()
        # update stat tables
        selected_record.update_stats(last_timestamp)
        return jsonify({
            "status" : "success",
            "msg" : "successfully delete selected record"
        })

        