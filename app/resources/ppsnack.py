from flask import request
from flask_restful import Resource
from app.models.ppcam import Ppcam

class PpsnackApi(Resource):
    def get(self, ppcam_id):
        selected_ppcam = Ppcam.query.filter_by(id = ppcam_id).first()
        if(selected_ppcam is None):
            return {
                "msg" : "ppcam not found"
            }, 404
        # request GET method to ppcam
        resp = selected_ppcam.get_ppsnack(test=True)
        return resp, 200

    def put(self, ppcam_id):
        selected_ppcam = Ppcam.query.filter_by(id=ppcam_id).first()
        if(selected_ppcam is None):
            return {
                "msg" : "ppcam not found"
            }, 404
        # request PUT method to ppcam
        feedback_ratio = request.json['feedback_ratio']
        if(selected_ppcam.put_ppsnack(feedback_ratio, test=True)):
            return {
                "msg":"Successfully change feedback ratio",
                "feedback_ratio":feedback_ratio
            }, 200
        else:
            return {
                "msg":"request to ppcam was failed",
                "feedback_ratio":feedback_ratio
            }, 500