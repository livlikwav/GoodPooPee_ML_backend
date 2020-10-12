from flask import json
from app.models.user import User
from app.models.ppcam_serial_nums import PpcamSerialNums
from flask import request, jsonify
from flask_restful import Resource
from app.models.ppcam import Ppcam
from app.utils.decorators import confirm_account
from app import db, ma
import datetime

class PpcamSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ppcam
        include_fk = True

# make instances of schemas
ppcam_schema = PpcamSchema()
ppcams_schema = PpcamSchema(many=True)

class PpcamRegisterApi(Resource):
    '''
    When first time to register ppcam profile to server
    Post ppcam profile to table
    '''
    def post(self):
        from sqlalchemy.exc import IntegrityError

        # check serial nums is valid
        exist_serial_record = PpcamSerialNums.query.filter_by(serial_num = request.json['serial_num']).first()
        if(exist_serial_record is None):
            return {
                "msg" : "Serial number is invalid. check again."
            }, 401
        # check user email is valid
        exist_user_record = User.query.filter_by(email = request.json['user_email']).first()
        if(exist_user_record is None):
            return {
                "msg" : "User email is invalid. check again."
            }, 401
        # create new ppcam profile
        new_ppcam = Ppcam(
            serial_num = request.json['serial_num'],
            ip_address = request.json['ip_address'],
            user_id = exist_user_record.id,
        )
        try:
            db.session.add(new_ppcam)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return {
                "msg" : "Fail to add new ppcam(IntegrityError)."
            }, 400
        return ppcam_schema.dump(new_ppcam), 200

class PpcamLoginApi(Resource):
    '''
    To issue device auth token
    '''
    def post(self):
        # check that ppcam profile exist
        login_device = Ppcam.query.filter_by(serial_num = request.json['serial_num']).first()
        if login_device is not None:
            device_auth_token = login_device.encode_auth_token(login_device.id)
            return {
                'device_access_token' : device_auth_token.decode('UTF-8')
            }, 200
        else:
            return {
                "msg" : "Serial number is invalid"
            }, 401
        

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
            return {
                "msg" : "IntegrityError on that ppcam, maybe pad of ppcam still exists."
            }, 409
        return {
            "msg" : "Successfully deleted that ppcam"
        }, 200
