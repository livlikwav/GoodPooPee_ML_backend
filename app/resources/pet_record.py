import logging
from app.utils.datetime import string_to_date, string_to_datetime
from flask import request
from flask_restful import Resource
from app.models.pet import Pet
from app.models.pet_record import DelPetRecordSchema, PetRecord, PetRecordSchema, RecordQuerySchema
from app.utils.decorators import confirm_account, confirm_device
from app import db
import datetime

# make instances of schemas
pet_record_schema = PetRecordSchema()
pet_records_schema = PetRecordSchema(many=True)
deleted_record_schema = DelPetRecordSchema()
record_query_schema = RecordQuerySchema()

class PetRecordApi(Resource):
    @confirm_device
    def post(self, pet_id: int):
        """
        Post new pet record by Ppcam(device)
        TEST by form-data, not raw JSON

        :Param pet_id: pet id of the record
        """
        from sqlalchemy.exc import IntegrityError
        logging.debug(request.form)

        # find user by pet_id
        selected_pet = Pet.query.filter_by(id = pet_id).first()
        # check 404
        if selected_pet is None:
            return {
                "msg" : "Pet not found"
            }, 404
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
            return {
                "msg" : "Fail to upload record image."
            }, 500
        # persistancy
        try:
            db.session.add(new_record)
            db.session.commit()
        except IntegrityError as e:
            new_record.delete_record_image()
            db.session.rollback()
            logging.error(f'POST: {e}')
            return {
                "msg" : "IntegrityError on post new pet_record, check primary keys"
            }, 409
        # update stat tables
        PetRecord.update_stats(new_record.pet_id, new_record.user_id, new_record.timestamp, string_to_datetime(request.form['timestamp']))
        return pet_record_schema.dump(new_record)

    @confirm_account
    def get(self, pet_id):
        # validate query string by ma
        errors = record_query_schema.validate(request.args)
        if errors:
            return {
                "msg" : "error in get method - query schema validation"
            }, 400
        # get timestamp in query string
        timestamp = request.args.get("timestamp")
        # get record by timestamp
        selected_record = PetRecord.query.filter_by(timestamp = timestamp, pet_id = pet_id).first()
        if(selected_record is None):
            return {
                "msg" : "Pet record not found"
            }, 404
        else:
            return pet_record_schema.dump(selected_record)


    @confirm_account
    def put(self, pet_id):
        from sqlalchemy.exc import IntegrityError
        # validate query string by ma
        errors = record_query_schema.validate(request.args)
        if errors:
            return {
                "status" : "fail",
                "msg" : "error in put method - query schema validation"
            }, 400
        # get old datetime in query string
        old_datetime = request.args.get("timestamp")
        # querying record
        selected_record = PetRecord.query.filter_by(timestamp = old_datetime, pet_id = pet_id).first()
        if(selected_record is None):
            return {
                "msg" : "Pet record not found"
            }, 404
        # update selected-record
        try:
            selected_record.timestamp = request.json['timestamp']
            selected_record.result = request.json['result']
            selected_record.last_modified_date = datetime.datetime.now()
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return {
                "msg" : "IntegrityError in put pet_record"
            }, 409
        # update stat tables
        PetRecord.update_stats(selected_record.pet_id, selected_record.user_id, selected_record.timestamp, string_to_datetime(old_datetime))
        return pet_record_schema.dump(selected_record)

    @confirm_account
    def delete(self, pet_id):
        from sqlalchemy.exc import IntegrityError
        # validate query string by ma
        errors = record_query_schema.validate(request.args)
        if errors:
            return {
                "msg" : "error in delete method - query schema validation"
            }, 400
        # get timestamp in query string
        old_datetime = request.args.get("timestamp")
        selected_record = PetRecord.query.filter_by(timestamp = old_datetime, pet_id = pet_id).first()
        # check 404
        if(selected_record is None):
            return {
                "msg" : "Pet record not found"
            }, 404
        deleted_pet_id = pet_id
        deleted_user_id = selected_record.user_id
        try:
            db.session.delete(selected_record)
            db.session.commit()
            # delete record image in S3
            selected_record.delete_record_image()
        except IntegrityError as e:
            db.session.rollback()
            return {
                "msg" : "IntegrityError of deleting pet record"
            }, 409
        # update stat tables
        PetRecord.update_stats(deleted_pet_id, deleted_user_id, string_to_datetime(old_datetime), string_to_datetime(old_datetime))
        return {
            "msg" : "successfully delete selected record"
        }, 200

class PetRecordsApi(Resource):
    @confirm_account
    def get(self, pet_id):
        '''
            /pet/<int:pet_id>/records
            Get all records at the date
            :Query param: timestamp: str
        '''
        # validate query string by ma
        errors = record_query_schema.validate(request.args)
        if errors:
            return {
                "msg" : "error in get method - query schema validation"
            }, 400
        # get timestamp in query string
        date = string_to_date(request.args.get("timestamp"))
        min_timestamp = datetime.datetime.combine(date, datetime.time.min)
        max_timestamp = datetime.datetime.combine(date, datetime.time.max)
        # get all records in that date
        selected_records = PetRecord.query.filter_by(pet_id = pet_id).\
            filter(PetRecord.timestamp <= max_timestamp).\
                filter(PetRecord.timestamp >= min_timestamp).\
                    all()
        if len(selected_records) == 0:
            return {
                "msg" : "Pet records not found"
            }, 404
        else:
            return pet_records_schema.dump(selected_records), 200