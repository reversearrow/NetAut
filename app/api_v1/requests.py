from flask import Blueprint, request, jsonify, make_response
from flask_restful import Resource
from ..models.requests import Requests, RequestSchema
from . import api

request_schema = RequestSchema()

class RequestListResource(Resource):
    '''
        Resource to post all requests and get new requests
    '''
    def get(self):
        all_requests = Requests.query.all()
        result = request_schema.dump(all_requests,many=True)
        return result

api.add_resource(RequestListResource, '/v1/requests/')
