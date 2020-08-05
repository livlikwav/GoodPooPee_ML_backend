from flask import request, jsonify
from flask_restful import Resource
from app.models.ppcam import Ppcam
from app import db, ma

# class PadApi(Resource):
#     def post(self, ppcam_id):
#         selected_ppcam = Ppcam.query.filter_by(id=ppcam_id).first()
#         # request POST method to ppcam
        