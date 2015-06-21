#!/usr/bin/env python

from os import environ
from urllib import urlencode
from datetime import datetime, timedelta

import requests


class Moves():

    AUTHORISE_URI = 'https://api.moves-app.com/oauth/v1/authorize'
    TOKEN_URI = 'https://api.moves-app.com/oauth/v1/access_token'
    SCOPE = 'location activity'
    AUTHORIZATION_CODE = 'authorization_code'
    REFRESH_TOKEN = 'refresh_token'

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def get_auth_uri(self, redirect_uri):
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': redirect_uri,
            'scope': self.SCOPE,
        }
        return '{0}?{1}'.format(self.AUTHORISE_URI, urlencode(params))

    def request_token(self, code, redirect_uri):
        data = {
            'grant_type': self.AUTHORIZATION_CODE,
            'code': code,
            'redirect_uri': redirect_uri,
        }
        return self._request_token(**data)

    def refresh_token(self, refresh_token, redirect_uri):
        data = {
            'grant_type': self.REFRESH_TOKEN,
            'refresh_token': refresh_token,
            'redirect_uri': redirect_uri,
        }
        return self._request_token(**data)

    def _request_token(self, **kwargs):
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        data.update(kwargs)
        r = requests.post(self.TOKEN_URI, data=data)
        res = r.json()
        print r.status_code
        expires_in = int(res['expires_in'])
        expires = datetime.now() + timedelta(seconds=expires_in)
        return res, expires
