from flask import Blueprint, request, jsonify, make_response, current_app
from flask_restful import  Resource
from sqlalchemy import exists
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from ...models import db
from ...models.requests import Requests, RequestSchema, RequestorEmails,RequestorEmailsSchema
from ...models.security.ip_blacklist import BlockedIPAddresses, BlockIPAddressSchema
from .. import api
import json, uuid, time
from .. import status
from rq import Queue, Connection
import redis

request_schema = RequestSchema()
block_ipaddress_schema = BlockIPAddressSchema()
email_schema = RequestorEmailsSchema()

class IPBlackList(Resource):
    def remove_duplicates_address(self,ips):
        for ip in ips:
            resp = BlockedIPAddresses.query.filter_by(ip_address=ip).all()
            print resp
            if resp:
                ips.remove(ip)
        return ips

    def get(self):
        requests = BlockedIPAddresses.query.all()
        result = block_ipaddress_schema.dump(requests,many=True)
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
            cleaned_ips = self.remove_duplicates_address(request_data['ip_addresses'])
            print cleaned_ips
            ret = BlockedIPAddresses.query.filter_by(ip_address='10.10.0.3').first()
            #ip_addresses = [BlockedIPAddresses(ip_address=ip_address) for ip_address in request_data['ip_addresses']]
            #emails = [RequestorEmails(email=email) for email in request_data['request']['notify']]
            #new_request = Requests()
            #new_request.import_data(request_data)
            #new_request.blockedipaddresses = ip_addresses
            #new_request.emails = emails
            #db.session.add(new_request)
            #db.session.commit()
            return status.HTTP_202_ACCEPTED
        except (SQLAlchemyError,IntegrityError) as error:
            response = {'error': error[0]}
            return response

api.add_resource(IPBlackList, '/v1/requests/blacklist/')
