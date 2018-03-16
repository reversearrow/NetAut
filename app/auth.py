from flask_httpauth import HTTPBasicAuth
from flask import jsonify, g
from models.users import Users

auth = HTTPBasicAuth()

@auth.verify_password
def verify_user_password(username, password):
    if username and password:
        g.user = Users.query.filter_by(username=username).first()
        if g.user is None:
            return False
        return g.user.verify_password(password)

@auth.error_handler
def unauthorized():
    response = jsonify({
            'status': 401,
            'error': 'unauthorized',
            'message': 'Please Authenticate'
        })
    response.status_code = 401
    return response
