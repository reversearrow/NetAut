from flask import Blueprint, request, jsonify, make_response, current_app,url_for
from flask_restful import  Resource
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from ...models import db
from ...models.requests import Requests, RequestSchema, RequestorEmails,RequestorEmailsSchema
from ...models.network.flush_cache import AkamaiFlushCache, AkamaiFlushCacheSchema, AkamaiFlushSchema
from .. import api
import json, uuid, time
from .. import status
from rq import Queue, Connection
import redis
from ...scripts.akamai.manage_cache import manage_cache

request_schema = RequestSchema(only=('request_number', 'creation_date','jobid','status','result'))
akamai_flush_schema = AkamaiFlushCacheSchema()
email_schema = RequestorEmailsSchema()
test_schema = AkamaiFlushSchema()

class AkamaiFlushCacheResource(Resource):
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
            with Connection(redis.from_url(current_app.config['REDIS_URL'])):
                q = Queue()
                job = q.enqueue(manage_cache,"Test",result_ttl=86400)
                new_request.jobid = job.id
            db.session.add(new_request)
            db.session.commit()
            #return status.HTTP_202_ACCEPTED, job.id
            return jsonify({'status': status.HTTP_202_ACCEPTED,
                    'jobid': job.id,
                    'result': url_for('api.resultsresource', id=job.id, _external=True, _scheme='https')
                    })
        except (SQLAlchemyError,IntegrityError) as error:
            response = {'error': error[0]}
            return response

api.add_resource(AkamaiFlushCacheResource, '/v1/requests/flushcache/')
