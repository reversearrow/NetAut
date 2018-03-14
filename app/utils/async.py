from flask import current_app
from rq import Queue, Connection
from rq.job import Job
import redis,time
from ..models import db
from ..models.requests import Requests


class ManageJobs:
    accepted_statues = ['finished','failed']
    
    def __init__(self,func=None,args=None):
        self.func = func
        self.args = args
        self.result_ttl = 86000

    def queue(self):
        with Connection(redis.from_url(current_app.config['REDIS_URL'])):
            q = Queue()
            job = q.enqueue_call(func=self.func,args=(self.args,),result_ttl=self.result_ttl)
            monitor = q.enqueue_call(func=self.monitor,args=(job.id,),result_ttl=self.result_ttl,depends_on=job.id)
            return job

    def monitor(self,id):
        job = Job.fetch(id)
        while job.status not in self.accepted_statues:
            time.sleep(1)
        else:
            request = Requests.query.filter_by(jobid=job.id).first()
            request.status = job.status
            db.session.add(request)
            db.session.commit()

    def get_job(self,id):
        with Connection(redis.from_url(current_app.config['REDIS_URL'])):
            job = Job.fetch(id)
            return job
