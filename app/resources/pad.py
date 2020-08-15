from flask import request, jsonify
from flask_restful import Resource
from app.models.pad import Pad
from app import db, ma
import datetime

class PadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pad
        include_fk = True

# make instances of schemas
pad_schema = PadSchema()
pads_schema = PadSchema(many=True)

class PadRegisterApi(Resource):
    def post(self, ppcam_id):
        from sqlalchemy.exc import IntegrityError
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
            return jsonify({
                "status" : "Fail",
                "msg" : "Fail to add new pad, its IntegrityError"
            })
        return pad_schema.dump(new_pad)

    def get(self, ppcam_id):
        selected_pads = Pad.query.filter_by(ppcam_id = ppcam_id).all()
        return pads_schema.dump(selected_pads)

class PadApi(Resource):
    def get(self, ppcam_id, pad_id):
        selected_pad = Pad.query.filter_by(ppcam_id = ppcam_id, id = pad_id).first()
        return pad_schema.dump(selected_pad)

    def put(self, ppcam_id, pad_id):
        from sqlalchemy.exc import IntegrityError
        selected_pad = Pad.query.filter_by(ppcam_id = ppcam_id, id = pad_id).first()
        try:
            selected_pad.lu = request.json['lu']
            selected_pad.ld = request.json['ld']
            selected_pad.ru = request.json['ru']
            selected_pad.rd = request.json['rd']
            selected_pad.last_modified_date = datetime.datetime.utcnow()
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({
                "status" : "Fail",
                "msg" : "IntegrityError on Pad<int:pad_id> Put method"
            })
        return pad_schema.dump(selected_pad)
    
    def delete(self, ppcam_id, pad_id):
        from sqlalchemy.exc import IntegrityError
        selected_pad = Pad.query.filter_by(ppcam_id = ppcam_id, id = pad_id).first()
        try:
            db.session.delete(selected_pad)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({
                "status" : "Fail",
                "msg" : "IntegrityError at pad profile, maybe primary key problem."
            })
        return jsonify({
            "status" : "Success",
            "msg" : "Successfully delete pad"
        })
        