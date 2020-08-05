from flask import request, jsonify
from flask_restful import Resource
from app.models.ppcam import Ppcam
from app import db, ma

class PpsnackApi(Resource):
    def get(self, ppcam_id):
        selected_ppcam = Ppcam.query.filter_by(id = ppcam_id).first()
        # request GET method to ppcam
        resp = selected_ppcam.get_ppsnack(test=True)
        return resp

    def put(self, ppcam_id):
        selected_ppcam = Ppcam.query.filter_by(id=ppcam_id).first()
        # request PUT method to ppcam
        feedback_ratio = request.json['feedback_ratio']
        if(selected_ppcam.put_ppsnack(feedback_ratio, test=True)):
            return jsonify({
                "status":"Success",
                "msg":"Successfully change feedback ratio",
                "feedback_ratio":feedback_ratio
            })
        else:
            return jsonify({
                "status":"Fail",
                "msg":"request to ppcam was failed",
                "feedback_ratio":feedback_ratio
            })

class PpsnackFeedingApi(Resource):
    def get(self, ppcam_id):
        selected_ppcam = Ppcam.query.filter_by(id=ppcam_id).first()
        # request GET method to ppcam
        if(selected_ppcam.get_ppsnack_feeding(test=True)):
            return jsonify({
                "status":"Success",
                "msg":"Successfully feed"
            })
        else:
            return jsonify({
                "status":"Fail",
                "msg":"feed request failed"
            })