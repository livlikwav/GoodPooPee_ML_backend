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
    @confirm_account
    def post(self):
        from sqlalchemy.exc import IntegrityError
        new_ppcam = Ppcam(
            serial_num = request.json['serial_num'],
            ip_address = request.json['ip_address'],
            # user_id is not nullable
            user_id = request.json['user_id']
        )
        try:
            db.session.add(new_ppcam)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({
                "status" : "fail",
                "msg" : "Fail to add new ppcam, its IntegrityError."
            })
        return ppcam_schema.dump(new_ppcam)

class PpcamApi(Resource):
    @confirm_account
    def get(self, ppcam_id):
        selected_ppcam = Ppcam.query.filter_by(id = ppcam_id).first()
        return ppcam_schema.dump(selected_ppcam)

    @confirm_account
    def put(self, ppcam_id):
        from sqlalchemy.exc import IntegrityError
        updated_ppcam = Ppcam.query.filter_by(id = ppcam_id).first()
        try:
            updated_ppcam.serial_num = request.json['serial_num']
            updated_ppcam.ip_address = request.json['ip_address']
            updated_ppcam.last_modified_date = datetime.datetime.utcnow()
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({
                "status" : "fail",
                "msg" : 'IntegrityError on updating ppcam'
            })
        return ppcam_schema.dump(updated_ppcam)

    @confirm_account
    def delete(self, ppcam_id):
        from sqlalchemy.exc import IntegrityError
        deleted_ppcam = Ppcam.query.filter_by(id = ppcam_id).first()
        try:
            db.session.delete(deleted_ppcam)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({
                "status" : "Fail",
                "msg" : "IntegrityError on that ppcam, maybe pad of ppcam still exists."
            })
        return jsonify({
            "status" : "Success",
            "msg" : "Successfully deleted that ppcam"
        })
