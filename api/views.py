from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from models import db, RequestAkamaiCCU, RequestSchema
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
import status, json


api_bp = Blueprint('api', __name__)
request_schema = RequestSchema()
api = Api(api_bp)

req1 = RequestAkamaiCCU(request_number='REQ123')
req2 = RequestAkamaiCCU(request_number='REQ345')

class RequestResource(Resource):
    def get(self):
        all_requests = RequestAkamaiCCU.query.all()
        result = request_schema.dump(all_requests,many=True)
        return result

    def patch(self,id):
        return {'hello': 'patched'}

    def post(self):
        request_data = request.get_json()
        if not request_data:
            response = {'message': 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST
        errors = request_schema.validate(request_data)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        try:
            request_number = request_data['request_number']
            new_request = RequestAkamaiCCU(request_number=request_number)
            db.session.add(new_request)
            db.session.commit()
        except (SQLAlchemyError,IntegrityError) as e:
            db.session.rollback()
            e = str(e)
            resp = {'error': e}
            return resp, status.HTTP_400_BAD_REQUEST


api.add_resource(RequestResource, '/messages/')
