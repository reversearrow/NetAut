from flask import Blueprint, request, jsonify, make_response, current_app,url_for
from flask_restful import  Resource
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from ...models import db
from ...models.requests import Requests, RequestSchema, RequestorEmails,RequestorEmailsSchema
from ...models.network.flush_cache import AkamaiFlushCache, AkamaiFlushCacheSchema, AkamaiFlushSchema
from .. import api
import json, uuid, time
from .. import status
from ...utils.async import ManageJobs
from ...scripts.akamai.manage_cache import manage_cache


request_schema = RequestSchema(only=('request_number', 'creation_date','jobid','status','result'))
akamai_flush_schema = AkamaiFlushCacheSchema()
email_schema = RequestorEmailsSchema()
test_schema = AkamaiFlushSchema()

class AkamaiFlushCacheListResource(Resource):
    def get(self):
        requests = Requests.query.filter_by(category='FlushCache').all()
        result = request_schema.dump(requests,many=True)
        return result

    def post(self):
        request_data = request.get_json()
        if not request_data:
            response = {'message': 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST
        errors = akamai_flush_schema.validate(request_data)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        try:
            cpcodes = [AkamaiFlushCache(cpcode=cpcode) for cpcode in request_data['cpcodes']]
            emails = [RequestorEmails(email=email) for email in request_data['request']['notify']]
            new_request = Requests()
            new_request.import_data(request_data)
            new_request.akamaiflushcache = cpcodes
            new_request.emails = emails
            new_job = ManageJobs(manage_cache,['25000'])
            job = new_job.queue()
            new_request.jobid = job.id
            new_request.status = job.status
            db.session.add(new_request)
            db.session.commit()
            return jsonify({'status': status.HTTP_202_ACCEPTED,
                    'job_status': job.status,
                    'job_id': job.id,
                    'result': url_for('api.resultsresource', id=job.id, _external=True),
                    'request': url_for('api.akamaiflushcacheresource', request_number=new_request.request_number, _external=True),
                    })
        except (SQLAlchemyError,IntegrityError) as error:
            response = {'error': error[0]}
            return response

class AkamaiFlushCacheResource(Resource):
    def get(self,request_number):
        requests = Requests.query.filter_by(request_number=request_number).first_or_404()
        result = request_schema.dump(requests)
        return result

api.add_resource(AkamaiFlushCacheListResource, '/v1/requests/flushcache/')
api.add_resource(AkamaiFlushCacheResource, '/v1/requests/flushcache/<string:request_number>')
