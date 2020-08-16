from flask import request, jsonify
from flask_restful import Resource
from app.models.pet import Pet
from app.models.pet_record import PetRecord
from app.utils.decorators import device_permission_required
from app import db, ma
import datetime

class PetRecordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PetRecord
        include_fk = True

class RecordQuerySchema(ma.Schema):
    class Meta:
        fields = ["timestamp"]


# make instances of schemas
pet_record_schema = PetRecordSchema()
# pet_records_schema = PetRecordSchema(many=True)
deleted_record_schema = PetRecordSchema(only=("timestamp", "pet_id", "user_id"))
record_query_schema = RecordQuerySchema()

class PetRecordApi(Resource):
    @device_permission_required
    def post(self, pet_id):
        """
        Post new pet record by Ppcam(device)
        TEST by form-data, not raw JSON

        :Param pet_id: pet id of the record
        """
        from sqlalchemy.exc import IntegrityError
        # find user by pet_id
        selected_pet = Pet.query.filter_by(id = pet_id).first()
        if not selected_pet:
            return jsonify({
                "status" : "Fail",
                "msg" : "Invalid pet_id"
            })
        # make new record object
        new_record = PetRecord(
            timestamp = request.form['timestamp'],
            result = request.form['result'],
            pet_id = pet_id,
            user_id = selected_pet.user_id
        )
        # Upload record image file
        image_uuid = new_record.upload_record_image(request.files['image'])
        if image_uuid:
            new_record.image_uuid = image_uuid
        else:
            return jsonify({
                "status" : "Fail",
                "msg" : "Fail to upload record image."
            })
        # persistancy
        try:
            db.session.add(new_record)
            db.session.commit()
        except IntegrityError as e:
            new_record.delete_record_image(image_uuid)
            db.session.rollback()
            return jsonify({
                "status" : "Fail",
                "msg" : "IntegrityError on post new pet_record, check primary keys"
            })
        # update stat tables
        new_record.update_stats(request.form['timestamp'])
        return pet_record_schema.dump(new_record)

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
        selected_record = PetRecord.query.filter_by(timestamp = timestamp, pet_id = pet_id).first()
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
        selected_record = PetRecord.query.filter_by(timestamp = last_timestamp, pet_id = pet_id).first()
        # update selected-record
        try:
            selected_record.timestamp = request.json['timestamp']
            selected_record.result = request.json['result']
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
        from sqlalchemy.exc import IntegrityError
        # validate query string by ma
        errors = record_query_schema.validate(request.args)
        if errors:
            return jsonify({
                "status" : "fail",
                "msg" : "error in delete method - query schema validation"
            })
        # get timestamp in query string
        last_timestamp = request.args.get("timestamp")
        selected_record = PetRecord.query.filter_by(timestamp = last_timestamp, pet_id = pet_id).first()
        try:
            db.session.delete(selected_record)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({
                "status" : "Fail",
                "msg" : "IntegrityError at deleting pet record"
            })
        # update stat tables
        selected_record.update_stats(last_timestamp)
        return jsonify({
            "status" : "success",
            "msg" : "successfully delete selected record"
        })