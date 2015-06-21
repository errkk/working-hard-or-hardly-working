#!/usr/bin/env python

from urllib import urlencode
from datetime import datetime, timedelta

import requests


class InvalidGrant(Exception):
    pass


class Moves():

    BASE_URI = 'https://api.moves-app.com/api/1.1'
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

    def refresh_token(self, refresh_token):
        data = {
            'grant_type': self.REFRESH_TOKEN,
            'refresh_token': refresh_token,
        }
        return self._request_token(**data)

    def _request_token(self, **kwargs):
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        data.update(kwargs)
        r = requests.post(self.TOKEN_URI, params=data)
        res = r.json()
        if 200 != r.status_code:
            raise InvalidGrant(r.content)
        expires_in = int(res['expires_in'])
        expires = datetime.now() + timedelta(seconds=expires_in)
        return res, expires
