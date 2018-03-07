from flask import Blueprint, request,current_app
from flask_restful import  Resource
from . import api
import json, uuid, time
from rq.job import Job
from webargs.flaskparser import parser
from webargs import fields
from rq import Queue, Connection
import redis

req_args = {
    'id': fields.Str(required=True),
}

class ResultsResource(Resource):
    def get(self):
        args = parser.parse(req_args,request)
        jobid = args['id']
        with Connection(redis.from_url(current_app.config['REDIS_URL'])):
            job = Job.fetch(jobid)
            print dir(job)
            print job.result
            return job.status
            #return jobid

api.add_resource(ResultsResource, '/v1/requests/results')
