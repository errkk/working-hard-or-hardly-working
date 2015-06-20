#!/usr/bin/env python
from os import environ
from os.path import join
from urllib import urlencode

import requests
from moves import MovesClient

from flask import Flask, render_template, request, redirect
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

BASE_URL = environ.get('BASE_URL')
MOVES_CLIENT_ID = environ.get('MOVES_CLIENT_ID')
MOVES_CLIENT_SECRET = environ.get('MOVES_CLIENT_SECRET')
MOVES_AUTHORISE_URI = 'https://api.moves-app.com/oauth/v1/authorize?'
MOVES_TOKEN_URI = 'https://api.moves-app.com/oauth/v1/access_token'

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('HEROKU_POSTGRESQL_WHITE_URL')
db = SQLAlchemy(app)

oauth2_params = {
    'response_type': 'code',
    'client_id': MOVES_CLIENT_ID,
    'redirect_uri': join(BASE_URL, 'redirect'),
    'scope': 'location activity',
}

@app.route('/')
def index():
    c = {
        'authorise_uri': MOVES_AUTHORISE_URI + urlencode(oauth2_params)
    }
    return render_template('index.html', **c)

@app.route('/redirect')
def redirect():
    code = request.args.get('code')
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': MOVES_CLIENT_ID,
        'client_secret': MOVES_CLIENT_SECRET,
        'redirect_uri': join(BASE_URL, 'redirect'),
    }
    r = requests.post(MOVES_TOKEN_URI, data=data)
    print r.json()
    data = r.json()
    return render_template('redirect.html', **data)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
