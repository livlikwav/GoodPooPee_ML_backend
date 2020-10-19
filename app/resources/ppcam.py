import logging
from app.models.pet import Pet
from app.models.user import User
from app.models.ppcam_serial_nums import PpcamSerialNums
from flask import request
from flask_restful import Resource
from app.models.ppcam import Ppcam, PpcamSchema
from app.utils.decorators import confirm_account
from app import db
import datetime

# make instances of schemas
ppcam_schema = PpcamSchema()
ppcams_schema = PpcamSchema(many=True)

class PpcamRegisterApi(Resource):
    def post(self):
        '''
        When first time to register ppcam profile to server
        Post ppcam profile to table
        :url: {{baseUrl}}/ppcam/register
        :body: serial_num: str, ip_address: str, user_id: int
        '''
        from sqlalchemy.exc import IntegrityError

        # check serial nums is valid
        exist_serial_record = PpcamSerialNums.query.filter_by(serial_num = request.json['serial_num']).first()
        if(exist_serial_record is None):
            return {
                "msg" : "Serial number is invalid. please check again."
            }, 404
        # check ppcam serial num already registered
        if(exist_serial_record.registered == 1):
            return {
                "msg" : "Serial number is already registered. please check again."
            }, 409
        # check user id is valid
        exist_user_record = User.query.filter_by(id = request.json['user_id']).first()
        if(exist_user_record is None):
            return {
                "msg" : "User id is invalid. please check again."
            }, 404
        # check that ppcam already exist
        exist_ppcam = Ppcam.query.filter_by(user_id = request.json['user_id']).first()
        if(exist_ppcam is not None):
            return {
                "msg" : "User's ppcam already exist. Please check again."
            }, 409
        # create new ppcam profile
        new_ppcam = Ppcam(
            serial_num = request.json['serial_num'],
            ip_address = request.json['ip_address'],
            user_id = request.json['user_id']
        )
        try:
            db.session.add(new_ppcam)
            # save that the serial number is used
            exist_serial_record.registered = 1
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.error(e)
            return {
                "msg" : "Fail to add new ppcam(IntegrityError)."
            }, 409
        return ppcam_schema.dump(new_ppcam), 200

class PpcamLoginApi(Resource):
    '''
    To issue device auth token for ppcam
    :path: None
    :body: serial_num: str
    '''
    def post(self):
        # check that ppcam profile exist
        login_device = Ppcam.query.filter_by(serial_num = request.json['serial_num']).first()
        if login_device is None:
            return {
                "msg" : "Registered ppcam not found"
            }, 404
        # check that user's pet exist
        user_id = login_device.user_id
        user_pet = Pet.query.filter_by(user_id = user_id).first()
        user_pet_id = 'null' # init user_pet_id by null
        if user_pet is not None:
            user_pet_id = user_pet.id
        # Issue device auth token
        device_auth_token = login_device.encode_auth_token(login_device.id)
        return {
            'device_access_token' : device_auth_token.decode('UTF-8'),
            'ppcam_id' : login_device.id,
            'user_id' : user_id,
            'pet_id' : user_pet_id
        }, 200

class PpcamApi(Resource):
    @confirm_account
    def get(self, ppcam_id):
        selected_ppcam = Ppcam.query.filter_by(id = ppcam_id).first()
        if(selected_ppcam is None):
            return {
                "msg" : "Ppcam not found"
            }, 404
        return ppcam_schema.dump(selected_ppcam), 200

    @confirm_account
    def put(self, ppcam_id):
        from sqlalchemy.exc import IntegrityError
        updated_ppcam = Ppcam.query.filter_by(id = ppcam_id).first()
        if(updated_ppcam is None):
            return {
                "msg" : "Ppcam not found"
            }, 404
        try:
            updated_ppcam.serial_num = request.json['serial_num']
            updated_ppcam.ip_address = request.json['ip_address']
            updated_ppcam.last_modified_date = datetime.datetime.utcnow()
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.error(e)
            return {
                "msg" : 'IntegrityError on updating ppcam'
            }, 409
        return ppcam_schema.dump(updated_ppcam), 200

    @confirm_account
    def delete(self, ppcam_id):
        from sqlalchemy.exc import IntegrityError
        deleted_ppcam = Ppcam.query.filter_by(id = ppcam_id).first()
        if(deleted_ppcam is None):
            return {
                "msg" : "Ppcam not found"
            }, 404
        try:
            db.session.delete(deleted_ppcam)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.error(e)
            return {
                "msg" : "IntegrityError on that ppcam, maybe pad of ppcam still exists."
            }, 409
        return {
            "msg" : "Successfully deleted that ppcam"
        }, 200
