from flask_restful import Resource
from app.utils.decorators import confirm_device
from app.models.ppcam import Ppcam

class PpcamPollingApi(Resource):
    @confirm_device
    def get(self, ppcam_id):
        '''
            /ppcam/<int:ppcam_id>/polling
            Polling request at every 3 seconds by ppcam
            :Request body: None
        '''
        ppcam = Ppcam.query.filter_by(id = ppcam_id).first()
        if(ppcam is None):
            return {
                "msg" : "Ppcam not found"
            }, 404

        # ===== Return queued request from app in redis =====

        # ==========

        # fake resp
        return {
            "msg" : "Fake succeess. Polling API not finished"
        }, 200