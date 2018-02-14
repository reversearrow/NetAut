from marshmallow import Schema, fields
from marshmallow import validate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import datetime

db = SQLAlchemy()
ma = Marshmallow()

class RequestsAddUpdate():
    def add_request(self,request):
        print "Adding Request from Parent Class"
        db.session.add(request)
        return db.session.commit()

class AddUpdateDelete():
    def add(self,resource):
        db.session.add(resource)
        return db.session.commit()

    def update(self,resource):
        return db.session.commit()

    def delete(self,resource):
        db.session.delete(resource)
        return db.session.commit()

class Requests(db.Model,RequestsAddUpdate):
    __tablename__ = 'requests'

    id = db.Column(db.Integer, primary_key=True)
    request_number = db.Column(db.String(20), unique=True, nullable=False)
    creation_date = db.Column(db.DateTime,default=datetime.datetime.utcnow,nullable=False)

    def __init__(self,request_number):
        self.request_number = request_number

class RequestorEmails(db.Model):
    __tablename__ = 'requestsoremails'

    id = db.Column(db.Integer, primary_key=True)
    request_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(40), nullable=False)

    def __init__(self,request_number,email):
        self.request_number = request_number
        self.email = email

class RequestCategories(db.Model):
    __tablename__ = 'requestcategories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    total_args = db.Column(db.Integer,nullable=False)

    def __init__(self,name,total_args):
        self.name = name
        self.total_args = total_args

class RequestSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    request_number = fields.String(required=True, validate=validate.Length(5))
    emails = fields.List(fields.Email(required=True),required=True)
    creation_date = fields.DateTime()
    category = fields.String(required=True)

class CategorySchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    total_args = fields.Integer(required=True)
