from app.utils.decorators import confirm_account
from app.models.ppsnack import Ppsnack, PpsnackSchema
from flask import request
from flask_restful import Resource
import datetime
from app import db

ppsnack_schema = PpsnackSchema()

class PpsnackApi(Resource):
    @confirm_account
    def get(self, ppcam_id):
        '''
            Return ppsnack data by ppcam id
        '''
        from sqlalchemy.exc import IntegrityError
        ppsnack = Ppsnack.query.filter_by(id = ppcam_id).first()
        if(ppsnack is None):
            return {
                "msg" : "ppsnack not found"
            }, 404
        return ppsnack_schema.dump(ppsnack), 200

    @confirm_account
    def put(self, ppcam_id):
        '''
            Update ppsnack data by request body
            - serial_num: str
            - feedback: float
        '''
        from sqlalchemy.exc import IntegrityError
        ppsnack = Ppsnack.query.filter_by(id=ppcam_id).first()
        if(ppsnack is None):
            return {
                "msg" : "ppsnack not found"
            }, 404
        try:
            ppsnack.serial_num = request.json['serial_num']
            ppsnack.feedback = request.json['feedback']
            ppsnack.last_modified_date = datetime.datetime.utcnow()
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return {
                "msg" : "IntegrityError on updating ppsnack"
            }, 409
        return ppsnack_schema.dump(ppsnack), 200