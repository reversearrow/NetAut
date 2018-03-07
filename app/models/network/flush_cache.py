from marshmallow import Schema, fields
from .. import db, ma
from ..requests import RequestSchema

class AkamaiFlushCache(db.Model):
    __tablename__ = 'akamai_flush_cache'
    id = db.Column(db.Integer, primary_key=True)
    #Todo: All CPCODES must be stored in different table and needs to be referenced here only.
    cpcode = db.Column(db.String(45), nullable=False)
    request_id = db.Column(db.Integer, db.ForeignKey('requests.uuidv4'), nullable=False)
    request = db.relationship('Requests', backref='akamaiflushcache', lazy=True)

class AkamaiFlushCacheSchema(ma.Schema):
    request = fields.Nested(RequestSchema,required=True)
    cpcodes = fields.List(fields.String(required=True),required=True)
    cpcode = fields.String()

class AkamaiFlushSchema(ma.Schema):
    request = fields.Nested(RequestSchema)
    akamaiflushcache = fields.Nested(AkamaiFlushCacheSchema,many=True)
    #cpcode = fields.String()
    # links = ma.Hyperlinks({
    #     'self': ma.URLFor('api.akamaiflushcacheresource', request='<request_number>', _scheme='https', _external=True),
    #     'collection': ma.URLFor('api.akamaiflushcacheresource', _scheme='https', _external=True),
    # })
