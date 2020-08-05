from flask import request
from flask_restful import Resource
from app.models.ppcam import Ppcam
from app import db, ma

class PpcamSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ppcam

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
        db.session.commit()
        return ppcam_schema.dump(updated_ppcam)

    def delete(self, ppcam_id):
        deleted_ppcam = Ppcam.query.filter_by(id = ppcam_id).first()
        db.session.delete(deleted_ppcam)
        db.session.commit()
        return '', 204
