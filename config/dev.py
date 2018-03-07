import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, '../db/data-dev-requests.db')

DEBUG = True
PORT = 5000
HOST = "0.0.0.0"
REDIS_URL = 'redis://localhost:6379/0'
QUEUES = ['default']
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_path
