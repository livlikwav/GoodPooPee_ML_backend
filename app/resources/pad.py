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
    def get(self, ppcam_id):
        '''
            ppcam/<int:ppcam_id>/pad
            Get pad profile
            :path: ppcam_id: int
            :body: None
        '''
        pad = Pad.query.filter_by(ppcam_id = ppcam_id).first()
        # check that pad exist
        if pad is None:
            return {
                "msg" : "Pad not found."
            }, 404
        return pad_schema.dump(pad), 200

    @confirm_account
    def put(self, ppcam_id):
        '''
            ppcam/<int:ppcam_id>/pad
            Put pad profile (Create new pad or update pad that exist)
            :path: ppcam_id: int
            :body: (int) ldx, ldy, lux, luy, rdx, rdy, rux, ruy
            :response code: 201 or 204
            *** Persist state of pad ***
        '''
        from sqlalchemy.exc import IntegrityError
        # Check that the ppcam exists first
        exist_ppcam = Ppcam.query.filter_by(id=ppcam_id).first()
        if (exist_ppcam is None):
            return {
                "msg" : "Ppcam not found"
            }, 404
        # check that pad
        pad = Pad.query.filter_by(ppcam_id = ppcam_id).first()
        if pad is None:
            # Create new pad
            self.is_pad_new = True
            pad = Pad(
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
            db.session.add(pad)
        else:
            # Update
            self.is_pad_new = False
            pad.lux = request.json['lux']
            pad.luy = request.json['luy']
            pad.ldx = request.json['ldx']
            pad.ldy = request.json['ldy']
            pad.rux = request.json['rux']
            pad.ruy = request.json['ruy']
            pad.rdx = request.json['rdx']
            pad.rdy = request.json['rdy']
            pad.last_modified_date = datetime.datetime.now()
        # Persistancy
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return {
                "msg" : "Fail to PUT pad profile(IntegrityError)."
            }, 409
        # Pad state management
        try:
            redis_client = RedisClient()
            redis_client.save_pad(ppcam_id=ppcam_id, data = json.dumps(pad_schema.dump(pad)))
        except Exception as e:
            logging.error(e)
            return {
                "msg" : "Fail to save pad state from redis"
            }, 409
        # Check proper status code
        if(self.is_pad_new):
            return pad_schema.dump(pad), 201
        else:
            return pad_schema.dump(pad), 204
    
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
