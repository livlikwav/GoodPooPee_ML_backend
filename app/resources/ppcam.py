from flask import request, jsonify
from flask_restful import Resource
from app.models.ppcam import Ppcam
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
    def post(self):
        new_ppcam = Ppcam(
            serial_num = request.json['serial_num'],
            # user_id is not nullable
            user_id = request.json['user_id']
        )
        db.session.add(new_ppcam)
        db.session.commit()
        return ppcam_schema.dump(new_ppcam)

class PpcamApi(Resource):
    def get(self, ppcam_id):
        selected_ppcam = Ppcam.query.filter_by(id = ppcam_id).first()
        return ppcam_schema.dump(selected_ppcam)

    def put(self, ppcam_id):
        updated_ppcam = Ppcam.query.filter_by(id = ppcam_id).first()
        updated_ppcam.serial_num = request.json['serial_num']
        updated_ppcam.last_modified_date = datetime.datetime.utcnow()
        db.session.commit()
        return ppcam_schema.dump(updated_ppcam)

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
