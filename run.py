#!/usr/bin/python
import os
from app import create_app
from app.auth import auth

app = create_app('dev')

@app.before_request
@auth.login_required
def before_request():
    pass

if __name__ == '__main__':
    app.run(host=app.config['HOST'],
            port=app.config['PORT'],
            debug=app.config['DEBUG'])
