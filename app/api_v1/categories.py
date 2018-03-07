from flask import Blueprint, request, jsonify, make_response
from flask_restful import Resource

class CategoriesResource(Resource):
    '''
        Resource to add new and get existing Categories.
    '''
    def get(self):
        all_categories = RequestCategories.query.all()
        #result = category_schema.dump(all_categories,many=True)
        #return result

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
