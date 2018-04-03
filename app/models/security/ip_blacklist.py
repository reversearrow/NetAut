from marshmallow import Schema, fields
from marshmallow import ValidationError, validates, validate
from .. import db, ma
from ..requests import RequestSchema

class BlockedIPAddresses(db.Model):
    __tablename__ = 'blocked_ip_addresses'
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(16),nullable=False,unique=True)
    request_id = db.Column(db.String, db.ForeignKey('requests.uuidv4'), nullable=False)
    request = db.relationship('Requests', backref='blockedipaddresses', lazy=True)

class BlockIPAddressSchema(ma.Schema):
    request = fields.Nested(RequestSchema,required=True)
    ip_address = fields.String()
    ip_addresses = fields.List(fields.String(validate=validate.Regexp('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')),required=True)

    @validates('ip_addresses')
    def validate_ip_addresses(self,ip_addresses):
        if ip_addresses == []:
            raise ValidationError("The list is empty.")
