import logging
from app.utils.datetime import string_to_datetime
from flask import request, jsonify
from flask_restful import Resource
from app.models.pet import Pet
from app.models.pet_record import PetRecord
from app.utils.decorators import device_permission_required, confirm_account
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
    # @device_permission_required
    def post(self, pet_id):
        """
        Post new pet record by Ppcam(device)
        TEST by form-data, not raw JSON

        :Param pet_id: pet id of the record
        """
        from sqlalchemy.exc import IntegrityError
        # find user by pet_id
        selected_pet = Pet.query.filter_by(id = pet_id).first()
        # check 404
        if selected_pet is None:
            return '', 404
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
            }), 500
        # persistancy
        try:
            db.session.add(new_record)
            db.session.commit()
        except IntegrityError as e:
            new_record.delete_record_image()
            db.session.rollback()
            logging.error(f'POST: {e}')
            return jsonify({
                "status" : "Fail",
                "msg" : "IntegrityError on post new pet_record, check primary keys"
            }), 409
        # update stat tables
        PetRecord.update_stats(new_record.pet_id, new_record.user_id, new_record.timestamp, string_to_datetime(request.form['timestamp']))
        return pet_record_schema.dump(new_record), 200

    @confirm_account
    def get(self, pet_id):
        # validate query string by ma
        errors = record_query_schema.validate(request.args)
        if errors:
            return jsonify({
                "status" : "fail",
                "msg" : "error in get method - query schema validation"
            }), 400
        # get timestamp in query string
        timestamp = request.args.get("timestamp")
        # get record by timestamp
        selected_record = PetRecord.query.filter_by(timestamp = timestamp, pet_id = pet_id).first()
        if(selected_record is None):
            return '',404
        else:
            return pet_record_schema.dump(selected_record)


    @confirm_account
    def put(self, pet_id):
        from sqlalchemy.exc import IntegrityError
        # validate query string by ma
        errors = record_query_schema.validate(request.args)
        if errors:
            return jsonify({
                "status" : "fail",
                "msg" : "error in put method - query schema validation"
            }), 400
        # get old datetime in query string
        old_datetime = request.args.get("timestamp")
        # querying record
        selected_record = PetRecord.query.filter_by(timestamp = old_datetime, pet_id = pet_id).first()
        if(selected_record is None):
            return '', 404
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
                "msg" : "IntegrityError in put pet_record"
            }), 409
        # update stat tables
        PetRecord.update_stats(selected_record.pet_id, selected_record.user_id, selected_record.timestamp, string_to_datetime(old_datetime))
        return pet_record_schema.dump(selected_record)

    @confirm_account
    def delete(self, pet_id):
        from sqlalchemy.exc import IntegrityError
        # validate query string by ma
        errors = record_query_schema.validate(request.args)
        if errors:
            return jsonify({
                "status" : "fail",
                "msg" : "error in delete method - query schema validation"
            }), 400
        # get timestamp in query string
        old_datetime = request.args.get("timestamp")
        selected_record = PetRecord.query.filter_by(timestamp = old_datetime, pet_id = pet_id).first()
        # check 404
        if(selected_record is None):
            return '', 404
        deleted_pet_id = pet_id
        deleted_user_id = selected_record.user_id
        try:
            db.session.delete(selected_record)
            db.session.commit()
            # delete record image in S3
            selected_record.delete_record_image()
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({
                "status" : "Fail",
                "msg" : "IntegrityError of deleting pet record"
            }), 409
        # update stat tables
        PetRecord.update_stats(deleted_pet_id, deleted_user_id, string_to_datetime(old_datetime), string_to_datetime(old_datetime))
        return jsonify({
            "status" : "success",
            "msg" : "successfully delete selected record"
        }), 200