from . import db, ma
from passlib.apps import custom_app_context as pwd_context
from marshmallow import ValidationError, validates, validate
from marshmallow import Schema, fields
import datetime


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))
    creation_date = db.Column(
        db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


class UsersSchema(ma.Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
