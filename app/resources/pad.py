from flask import request
from flask_restful import Resource
from app.models.pad import Pad, PadSchema
from app.utils.decorators import confirm_account
from app import db
import datetime

# make instances of schemas
pad_schema = PadSchema()
pads_schema = PadSchema(many=True)

class PadApi(Resource):
    @confirm_account
    def post(self, ppcam_id):
        from sqlalchemy.exc import IntegrityError
        existed_pad = Pad.query.filter_by(ppcam_id=ppcam_id).first()
        if existed_pad:
            return {
                "status" : "Fail",
                "msg" : "Pad profile already exists in that ppcam."
            }, 409
            
        new_pad = Pad(
            lu = request.json['lu'],
            ld = request.json['ld'],
            ru = request.json['ru'],
            rd = request.json['rd'],
            user_id = request.json['user_id'],
            ppcam_id = ppcam_id
        )
        try:
            db.session.add(new_pad)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return {
                "status" : "Fail",
                "msg" : "IntegrityError"
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
