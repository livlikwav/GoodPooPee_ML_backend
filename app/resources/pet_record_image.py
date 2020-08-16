from flask import request, jsonify, Response
from flask_restful import Resource
from app.models.pet_record import PetRecord
from app.utils.s3 import get_object
from app import db, ma

class PetRecordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PetRecord
        include_fk = True

class RecordQuerySchema(ma.Schema):
    class Meta:
        fields = ["timestamp"]


# make instances of schemas
pet_record_schema = PetRecordSchema()
record_query_schema = RecordQuerySchema()

class PetRecordImageApi(Resource):
    def get(self, pet_id):
        """
        Get pet record image in S3
        
        :Param pet_id: pet id of the record image
        :QueryString: Timestamp of the record
        """
        # validate query string by ma
        errors = record_query_schema.validate(request.args)
        if errors:
            return jsonify({
                "status" : "fail",
                "msg" : "error in put method - query schema validation"
            })
        # get timestamp in query string
        last_timestamp = request.args.get("timestamp")
        # querying record
        selected_record = PetRecord.query.filter_by(timestamp = last_timestamp, pet_id = pet_id).first()
        # 
        image_uuid = selected_record.image_uuid
        file_data = get_object(image_uuid)
        if file_data:
            return Response(
                file_data,
                mimetype='image/png'
            )
        else:
            return jsonify({
                "status" : "Fail",
                "msg" : "Fail to get object from S3 bucket."
            })