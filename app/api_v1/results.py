from flask import Blueprint, request, current_app, jsonify
from flask_restful import  Resource
from . import api
import json, uuid, time
from rq.job import Job
from rq import Queue, Connection
import redis


class ResultsResource(Resource):
    def get(self,id):
        jobid = id
        with Connection(redis.from_url(current_app.config['REDIS_URL'])):
            job = Job.fetch(jobid)
            print job.get_status()
            print job.result
            return jsonify({
                    'result': job.result,
                    'status': job.status
                })
            #return jobid

api.add_resource(ResultsResource, '/v1/requests/results/<string:id>')
