from flask import Blueprint, request, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from ..models.users import Users, UsersSchema
from . import api, status
from ..models import db

user_schema = UsersSchema()

class UsersResource(Resource):
    def post(self):
        request_data = request.get_json()
        if not request_data:
            response = {'message': 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST
        errors = user_schema.validate(request_data)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        try:
            username = request_data['username']
            password = request_data['password']
            if Users.query.filter_by(username = username).first() is not None:
                return "User already exists!" , status.HTTP_400_BAD_REQUEST
            user = Users(username = username)
            user.hash_password(password)
            db.session.add(user)
            db.session.commit()
            return status.HTTP_201_CREATED
        except (SQLAlchemyError,IntegrityError) as error:
            response = {'error': error[0]}
            return response

api.add_resource(UsersResource, '/v1/users/')
