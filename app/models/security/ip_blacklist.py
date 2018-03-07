from marshmallow import Schema, fields
from marshmallow import validate, post_dump, ValidationError, validates
from .. import db, ma
from ..requests import RequestSchema

class BlockedIPAddresses(db.Model):
    __tablename__ = 'blocked_ip_addresses'
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(16),nullable=False,unique=True)
    request_id = db.Column(db.Integer, db.ForeignKey('requests.uuidv4'), nullable=False)
    request = db.relationship('Requests', backref='blockedipaddresses', lazy=True)

class BlockIPAddressSchema(ma.Schema):
    request = fields.Nested(RequestSchema,required=True)
    ip_address = fields.String()
    ip_addresses = fields.List(fields.String(required=True),required=True)
