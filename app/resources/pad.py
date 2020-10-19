import logging
from app.models.redis_client import RedisClient
from app.models.ppcam import Ppcam
from flask import request
from flask_restful import Resource
from app.models.pad import Pad, PadSchema
from app.utils.decorators import confirm_account
from app import db
import datetime
import json

# make instances of schemas
pad_schema = PadSchema()

class PadApi(Resource):
    @confirm_account
    def post(self, ppcam_id):
        '''
            ppcam/<int:ppcam_id>/pad
            Set pad profile by user, not ppcam
            :path: ppcam_id: int
            :body: (int) ldx, ldy, lux, luy, rdx, rdy, rux, ruy
            *** Persist state of pad ***
        '''
        from sqlalchemy.exc import IntegrityError
        # check that ppcam exist
        exist_ppcam = Ppcam.query.filter_by(id=ppcam_id).first()
        if (exist_ppcam is None):
            return {
                "msg" : "Invalid ppcam id. please check again."
            }, 404
        # check that pad already exist
        exist_pad = Pad.query.filter_by(ppcam_id=ppcam_id).first()
        if (exist_pad is not None):
            return {
                "msg" : "Ppcam's pad already exist. Please check again."
            }, 409
        # Create new pad profile
        new_pad = Pad(
            lux = request.json['lux'],
            luy = request.json['luy'],
            ldx = request.json['ldx'],
            ldy = request.json['ldy'],
            rux = request.json['rux'],
            ruy = request.json['ruy'],
            rdx = request.json['rdx'],
            rdy = request.json['rdy'],
            ppcam_id = ppcam_id,
            user_id = exist_ppcam.user_id
        )
        try:
            db.session.add(new_pad)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.error(e)
            return {
                "msg" : "Fail to add new pad profile(IntegrityError)"
            }, 409
        # *** Persist state of pad ***
        try:
            redis_client = RedisClient()
            redis_client.save_pad(ppcam_id=ppcam_id, data = json.dumps(pad_schema.dump(new_pad)))
        except Exception as e:
            logging.error(e)
            return {
                "msg" : "Fail to save pad state from redis"
            }, 409
        return pad_schema.dump(new_pad), 200

    @confirm_account
    def get(self, ppcam_id):
        '''
            ppcam/<int:ppcam_id>/pad
            Get pad profile
            :path: ppcam_id: int
            :body: None
        '''
        selected_pad = Pad.query.filter_by(ppcam_id = ppcam_id).first()
        # check that pad exist
        if selected_pad is None:
            return {
                "msg" : "Pad not found."
            }, 404
        return pad_schema.dump(selected_pad), 200

    @confirm_account
    def put(self, ppcam_id):
        '''
            ppcam/<int:ppcam_id>/pad
            Put pad profile
            :path: ppcam_id: int
            :body: (int) ldx, ldy, lux, luy, rdx, rdy, rux, ruy
            *** Persist state of pad ***
        '''
        from sqlalchemy.exc import IntegrityError
        selected_pad = Pad.query.filter_by(ppcam_id = ppcam_id).first()
        # check that pad exist
        if selected_pad is None:
            return {
                "msg" : "Pad not found."
            }, 404
        # put new pad profile
        try:
            selected_pad.lux = request.json['lux']
            selected_pad.luy = request.json['luy']
            selected_pad.ldx = request.json['ldx']
            selected_pad.ldy = request.json['ldy']
            selected_pad.rux = request.json['rux']
            selected_pad.ruy = request.json['ruy']
            selected_pad.rdx = request.json['rdx']
            selected_pad.rdy = request.json['rdy']
            selected_pad.last_modified_date = datetime.datetime.utcnow()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return {
                "msg" : "Fail to update pad profile(IntegrityError)."
            }, 409
        # *** Persist state of pad ***
        try:
            redis_client = RedisClient()
            redis_client.save_pad(ppcam_id=ppcam_id, data = json.dumps(pad_schema.dump(selected_pad)))
        except Exception as e:
            logging.error(e)
            return {
                "msg" : "Fail to save pad state from redis"
            }, 409
        return pad_schema.dump(selected_pad), 200
    
    @confirm_account
    def delete(self, ppcam_id):
        '''
            ppcam/<int:ppcam_id>/pad
            Delete pad profile
            :path: ppcam_id: int
            :body: None
        '''
        from sqlalchemy.exc import IntegrityError
        selected_pad = Pad.query.filter_by(ppcam_id = ppcam_id).first()
        # Check that pad exists
        if selected_pad is None:
            return {
                "msg" : "Pad not found."
            }, 404
        try:
            db.session.delete(selected_pad)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.error(e)
            return {
                "msg" : "Fail to delete pad(IntegrityError)."
            }, 409
        return {
            "msg" : "Success to delete pad"
        }, 200
