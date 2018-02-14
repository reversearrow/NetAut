from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from models import db, Requests, RequestorEmails, RequestCategories, CategorySchema, RequestSchema
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
import status, json


api_bp = Blueprint('api', __name__)
request_schema = RequestSchema()
category_schema = CategorySchema()
api = Api(api_bp)



class CategoriesResource(Resource):
    def get(self):
        all_categories = RequestCategories.query.all()
        result = category_schema.dump(all_categories,many=True)
        return result

    def post(self):
        request_data = request.get_json()
        if not request_data:
            response = {'message': 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST
        errors = category_schema.validate(request_data)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        try:
            category = request_data['category']
            args = request_data['args']
            q = db.session.query(RequestCategories).filter_by(name=category).first()
            if not q:
                new_req_category = RequestCategories(name=category,total_args=args)
                db.session.add(new_req_category)
                db.session.commit()
            else:
                return "Category already exists"
        except (SQLAlchemyError) as e:
            return e


class RequestResource(Resource):
    def get(self):
        all_requests = Requests.query.all()
        result = request_schema.dump(all_requests,many=True)
        return result

    def patch(self,id):
        return {'hello': 'patched'}

    def post(self):
        request_data = request.get_json()
        if not request_data:
            response = {'message': 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST
        errors = request_schema.validate(request_data)
        if errors:
            return errors, status.HTTP_400_BAD_REQUEST
        try:
            request_number = request_data['request_number']
            emails = request_data['emails']
            new_request = Requests(request_number=request_number)
            for email in emails:
                req_emails = RequestorEmails(request_number=request_number,email=email)
                db.session.add(req_emails)
            new_request.add_request(new_request)
            #db.session.add(new_request)
            #db.session.commit()
        except (SQLAlchemyError,IntegrityError) as e:
            db.session.rollback()
            e = str(e)
            print e
        #    resp = {'error': e}
        #    return resp, status.HTTP_400_BAD_REQUEST


api.add_resource(RequestResource, '/requests/')
api.add_resource(CategoriesResource, '/requests/categories/')
#api.add_resource(, '/requests/<string:category>/')
