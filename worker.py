from run import app
from flask_script import Manager
from rq import Connection, Worker
import redis

manager = Manager(app)


@manager.command
def run_worker():
    redis_url = app.config['REDIS_URL']
    redis_connection = redis.from_url(redis_url)
    with Connection(redis_connection):
        worker = Worker(app.config['QUEUES'])
        worker.work()


if __name__ == "__main__":
    manager.run()
