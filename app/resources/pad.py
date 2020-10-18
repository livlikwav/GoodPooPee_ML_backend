from app.models.ppcam import Ppcam
from flask import request
from flask_restful import Resource
from app.models.pad import Pad, PadSchema
from app.utils.decorators import confirm_account
from app import db
import datetime

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
            return {
                "msg" : "Fail to add new pad profile(IntegrityError)"
            }, 409
        return pad_schema.dump(new_pad), 200

    @confirm_account
    def get(self, ppcam_id):
        selected_pad = Pad.query.filter_by(ppcam_id = ppcam_id).first()

        if not selected_pad:
            return {
                "status" : "Fail",
                "msg" : "Pad not found."
            }, 404

        return pad_schema.dump(selected_pad), 200

    @confirm_account
    def put(self, ppcam_id):
        from sqlalchemy.exc import IntegrityError
        selected_pad = Pad.query.filter_by(ppcam_id = ppcam_id).first()

        if not selected_pad:
            return {
                "status" : "Fail",
                "msg" : "Pad not found."
            }, 404

        try:
            selected_pad.lu = request.json['lu']
            selected_pad.ld = request.json['ld']
            selected_pad.ru = request.json['ru']
            selected_pad.rd = request.json['rd']
            selected_pad.last_modified_date = datetime.datetime.utcnow()
            db.session.commit()
        except:
            db.session.rollback()
            return {
                "status" : "Fail",
                "msg" : "IntegrityError"
            }, 400
        return pad_schema.dump(selected_pad), 200
    
    @confirm_account
    def delete(self, ppcam_id):
        from sqlalchemy.exc import IntegrityError
        selected_pad = Pad.query.filter_by(ppcam_id = ppcam_id).first()

        if not selected_pad:
            return {
                "status" : "Fail",
                "msg" : "Pad not found."
            }, 404

        try:
            db.session.delete(selected_pad)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return {
                "status" : "Fail",
                "msg" : "IntegrityError"
            }, 409
        return {
            "status" : "Success",
            "msg" : "Successfully delete pad"
        }, 200
