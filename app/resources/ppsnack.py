import logging
from app.models.redis_client import RedisClient
from app.models.ppcam import Ppcam
from app.models.ppsnack_serial_nums import PpsnackSerialNums
from app.utils.decorators import confirm_account, confirm_device
from app.models.ppsnack import Ppsnack, PpsnackSchema
from flask import request
from flask_restful import Resource
import datetime
from app import db
import json

ppsnack_schema = PpsnackSchema()

class PpsnackApi(Resource):
    @confirm_device
    def post(self, ppcam_id):
        '''
            /ppcam/<int:ppcam_id>/ppsnack
            Register ppsnack by ppcam
            :path: ppcam_id: int
            :body: serial_num: str, feedback: float
            *** Persist state of ppsnack ***
        '''
        from sqlalchemy.exc import IntegrityError

        # check serial nums is valid
        exist_serial = PpsnackSerialNums.query.filter_by(serial_num = request.json['serial_num']).first()
        if(exist_serial is None):
            return {
                "msg" : "Serial number is invalid. Please check again."
            }, 404
        # check ppsnack serial num already registered
        if(exist_serial.registered == 1):
            return {
                "msg" : "Serial number is already registered. please check again."
            }, 409
        # check ppcam id is valid
        exist_ppcam = Ppcam.query.filter_by(id = ppcam_id).first()
        if(exist_ppcam is None):
            return {
                "msg" : "Ppcam id is invalid. please check again."
            }, 404
        # create new ppsnack profile
        new_ppsnack = Ppsnack(
            serial_num = request.json['serial_num'],
            feedback = request.json['feedback'],
            ppcam_id = ppcam_id,
            user_id = exist_ppcam.user_id
        )
        try:
            db.session.add(new_ppsnack)
            # save that the serial number is used
            exist_serial.registered = 1
            db.session.commit()
            # *** Persist state of ppsnack ***
            redis_client = RedisClient()
            redis_client.save_ppsnack(ppcam_id=ppcam_id, data=json.dumps(ppsnack_schema.dump(new_ppsnack)))
        except IntegrityError as e:
            db.session.rollback()
            return {
                "msg" : "Fail to add new ppcam(IntegrityError)."
            }, 409
        # Return response
        return ppsnack_schema.dump(new_ppsnack), 200

    @confirm_account
    def get(self, ppcam_id):
        '''
            Return ppsnack data by ppcam id
            :path: ppcam_id: int
            :body: None
        '''
        ppsnack = Ppsnack.query.filter_by(ppcam_id = ppcam_id).first()
        if(ppsnack is None):
            return {
                "msg" : "ppsnack not found"
            }, 404
        return ppsnack_schema.dump(ppsnack), 200

    @confirm_account
    def put(self, ppcam_id):
        '''
            Update ppsnack data by request body
            :path: ppcam_id: int
            :body: feedback: float
            *** Persist state of ppsnack ***
        '''
        from sqlalchemy.exc import IntegrityError
        ppsnack = Ppsnack.query.filter_by(ppcam_id=ppcam_id).first()
        if(ppsnack is None):
            return {
                "msg" : "ppsnack not found"
            }, 404
        try:
            ppsnack.feedback = request.json['feedback']
            ppsnack.last_modified_date = datetime.datetime.utcnow()
            db.session.commit()
            # *** Persist state of ppsnack ***
            redis_client = RedisClient()
            redis_client.save_ppsnack(ppcam_id=ppcam_id, data=json.dumps(ppsnack_schema.dump(ppsnack)))
        except IntegrityError as e:
            db.session.rollback()
            return {
                "msg" : "IntegrityError on updating ppsnack"
            }, 409
        return ppsnack_schema.dump(ppsnack), 200


class PpsnackFeedApi(Resource):
    @confirm_account
    def post(self, ppcam_id):
        '''
            /ppcam/<int:ppcam_id>/ppsnack/feeding
            Signal ppsnack to feed pet
            :path: ppcam_id: int
            :body: None
            *** Persist state of feeding ***
        '''
        # check ppsnack is valid
        ppsnack = Ppsnack.query.filter_by(ppcam_id = ppcam_id).first()
        if (ppsnack is None):
            return {
                "msg" : "ppsnack not found"
            }, 404
        # Set state of feeding
        try:
            redis_client = RedisClient()
            resp = redis_client.save_feeding(ppcam_id=ppcam_id)
        except Exception as e:
            logging.error(e)
            return {
                "msg" : "Fail to save feeding state"
            }, 409
        if(resp is None):
            return {
                "msg" : "Error on saving feeding state"
            }, 500
        return resp, 200