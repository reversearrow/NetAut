from marshmallow import Schema, fields
from marshmallow import validate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import datetime

db = SQLAlchemy()
ma = Marshmallow()

class AddUpdateDelete():
    def add(self,resource):
        db.session.add(resource)
        return db.session.commit()

    def update(self,resource):
        return db.session.commit()

    def delete(self,resource):
        db.session.delete(resource)
        return db.session.commit()

class RequestAkamaiCCU(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_number = db.Column(db.String(20), unique=True, nullable=False)
    creation_date = db.Column(db.DateTime,default=datetime.datetime.utcnow,nullable=False)
    # Add Email of the Requester
    # Add CPCODES/URL Requested
    def __init__(self,request_number):
        self.request_number = request_number

    def __repr__(self):
        return '<Request %r>' % self.request_number


class RequestSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    request_number = fields.String(required=True, validate=validate.Length(5))
    creation_date = fields.DateTime()
    #url = ma.URLFor('')
