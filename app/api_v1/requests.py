from flask import Blueprint, request, jsonify, make_response
from flask_restful import Resource

from . import api

class RequestListResource(Resource):
    '''
        Resource to post all requests and get new requests
    '''
    def get(self):
        all_requests = Requests.query.all()
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
            emails = request_data['emails']
            new_request = Requests(request_number=request_number)
            for email in emails:
                req_emails = RequestorEmails(request_number=request_number,email=email)
                db.session.add(req_emails)
            new_request.add_request(new_request)
            #db.session.add(new_request)
            #db.session.commit()
        except (SQLAlchemyError,IntegrityError) as e:
            db.session.rollback()
            e = str(e)
            print e
        #    resp = {'error': e}
        #    return resp, status.HTTP_400_BAD_REQUEST


class RequestResource(Resource):
    def get(self,id):
        print id
