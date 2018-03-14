from flask import Blueprint, request, jsonify, make_response, current_app, url_for
from flask_restful import  Resource
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from ...models import db
from ...models.requests import Requests, RequestSchema, RequestorEmails,RequestorEmailsSchema
from ...models.security.ip_blacklist import BlockedIPAddresses, BlockIPAddressSchema
from .. import api
import json, uuid, time
from .. import status
from ...utils.async import ManageJobs
from ...scripts.akamai.manage_cache import manage_cache

request_schema = RequestSchema(only=('request_number', 'creation_date','jobid','status','result'))
block_ipaddress_schema = BlockIPAddressSchema()
email_schema = RequestorEmailsSchema()

class IPBlackList(Resource):
    def get(self):
        requests = Requests.query.filter_by(category='IPBlacklist').all()
        result = request_schema.dump(requests,many=True)
        #requests = BlockedIPAddresses.query.all()
        # result = block_ipaddress_schema.dump(requests,many=True)
        return result

    def post(self):
        request_data = request.get_json()
        if not request_data:
            response = {'message': 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST
        errors = block_ipaddress_schema.validate(request_data)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        if request_data['request']['category'] != 'IPBlacklist':
            return 'Invalid Category', status.HTTP_400_BAD_REQUEST
        try:
            ip_addresses = [BlockedIPAddresses(ip_address=ip_address) for ip_address in [ip for ip in request_data['ip_addresses'] if not BlockedIPAddresses.query.filter_by(ip_address=ip).first()]]
            if ip_addresses == []:
                return 'IPs Already Exists|', status.HTTP_400_BAD_REQUEST
            emails = [RequestorEmails(email=email) for email in request_data['request']['notify']]
            new_request = Requests()
            new_request.import_data(request_data)
            new_request.blockedipaddresses = ip_addresses
            new_request.emails = emails
            manage_jobs = ManageJobs(manage_cache,['25000'])
            job = manage_jobs.queue()
            new_request.jobid = job.id
            new_request.status = job.status
            db.session.add(new_request)
            db.session.commit()
            return jsonify({'status': status.HTTP_202_ACCEPTED,
                    'job_status': job.status,
                    'job_id': job.id,
                    'result': url_for('api.resultsresource', id=job.id, _external=True),
                    'request': url_for('api.ipblacklist', request_number=new_request.request_number, _external=True),
                    })
        except (SQLAlchemyError,IntegrityError) as error:
            response = {'error': error[0]}
            return response

class IPBlackListResource(Resource):
    def get(self,request_number):
        requests = Requests.query.filter_by(request_number=request_number).first_or_404()
        result = request_schema.dump(requests)
        return result

api.add_resource(IPBlackList, '/v1/requests/blacklist/')
api.add_resource(IPBlackListResource, '/v1/requests/blacklist/<string:request_number>')
