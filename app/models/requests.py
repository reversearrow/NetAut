from marshmallow import Schema, fields
from marshmallow import validate, post_dump, ValidationError, validates
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from . import db, ma
import datetime
import uuid



class Requests(db.Model):
    __tablename__ = 'requests'

    request_number = db.Column(db.String(20), unique=True, nullable=False)
    creation_date = db.Column(db.DateTime,default=datetime.datetime.utcnow,nullable=False)
    category = db.Column(db.String(30),nullable=False)
    status = db.Column(db.String(30),nullable=False)
    uuidv4 = db.Column(db.String(64),nullable=False,primary_key=True)
    jobid = db.Column(db.String(64),nullable=False)

    def import_data(self,data):
        try:
            self.request_number = data['request']['request_number']
            self.category = data['request']['category']
            self.uuidv4 = uuid.uuid4().hex
        except:
            return "Exception"
        return self

class RequestorEmails(db.Model):
    __tablename__ = 'requestsor_emails'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), nullable=False)
    request_id = db.Column(db.Integer, db.ForeignKey('requests.uuidv4'), nullable=False)
    request = db.relationship('Requests', backref='emails', lazy=True)

    def __init__(self,email):
        self.email = email

class RequestorEmailsSchema(ma.Schema):
    request_number = fields.String(required=True)
    email = fields.String(required=True)
    request_id = fields.String(required=True)


class RequestSchema(ma.Schema):
    request_number = fields.String(required=True, validate=validate.Length(5))
    notify = fields.List(fields.Email(),required=True)
    creation_date = fields.DateTime()
    category = fields.String(required=True)
    status = fields.String()
    jobid = fields.String()
    emails = fields.Nested(RequestorEmailsSchema,many=True,exclude=('request_id'))
    result = ma.URLFor('api.resultsresource', id='<jobid>', _external=True, _scheme='http')

    @validates('category')
    def validate_category(self,category):
        categories = ["FlushCache","IPBlacklist","IPWhitelist"]
        if category not in categories:
            raise ValidationError("Invalid Category")

    @validates('notify')
    def validate_emails(self,notify):
        if notify == []:
            raise ValidationError("Please enter email to notify.")
