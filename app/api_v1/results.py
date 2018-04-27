from flask import jsonify
from flask_restful import Resource
from . import api
from ..utils.async import ManageJobs


class ResultsResource(Resource):
    def get(self, id):
        managejobs = ManageJobs()
        job = managejobs.get_job(id)
        return jsonify({
            'result': job.result,
            'status': job.status
        })


api.add_resource(ResultsResource, '/v1/requests/results/<string:id>')
