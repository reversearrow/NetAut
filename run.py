#!/usr/bin/python
import os
from app import create_app

app = create_app('dev')

if __name__ == '__main__':
    app.run(host=app.config['HOST'],
            port=app.config['PORT'],
            debug=app.config['DEBUG'])
