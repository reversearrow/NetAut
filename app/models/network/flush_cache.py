from marshmallow import Schema, fields, validates, ValidationError
from .. import db, ma
from ..requests import RequestSchema


class AkamaiFlushCache(db.Model):
    __tablename__ = 'akamai_flush_cache'
    id = db.Column(db.Integer, primary_key=True)
    # Todo: All CPCODES must be stored in different table and needs to be referenced here only.
    cpcode = db.Column(db.String(45), nullable=False)
    request_id = db.Column(db.Integer, db.ForeignKey(
        'requests.uuidv4'), nullable=False)
    request = db.relationship(
        'Requests', backref='akamaiflushcache', lazy=True)


class AkamaiFlushCacheSchema(ma.Schema):
    request = fields.Nested(RequestSchema, required=True)
    cpcodes = fields.List(fields.String(), required=True)
    cpcode = fields.String()

    @validates('cpcodes')
    def validate_cpcodes(self, cpcodes):
        if cpcodes == []:
            raise ValidationError("The list is empty.")
