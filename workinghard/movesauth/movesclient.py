#!/usr/bin/env python

import operator
from urllib import urlencode
from datetime import datetime, timedelta
from dateutil import parser

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

    DAILY = '/user/places/daily?'

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


class MovesSegment:
    def __init__(self, **kwargs):
        self.might_be_work = 0

        for (k, v) in kwargs.iteritems():
            setattr(self, k, v)

        if hasattr(self, 'startTime') and hasattr(self, 'endTime'):
            self._parse_datestrings()

        self.place_id = int(self.place['id'])

        if self.name and self.name in ['work', 'office']:
            self.might_be_work += 2
        if self.place['type'].lower == 'work':
            self.might_be_work += 2
        if self.duration > timedelta(hours=7):
            self.might_be_work += 1

    def _parse_datestrings(self):
        self.start = parser.parse(self.startTime)
        self.end = parser.parse(self.endTime)
        self.duration = self.end - self.start
        self.name = self.place.get('name', None)
        self.name = self.name.lower() if self.name else None



class MovesSegmentList:
    def __init__(self, items):
        self.segments = []
        self.place_times = {}
        self.places = {}

        for day in items:
            for item in day['segments']:
                segment = MovesSegment(**item)
                self.segments.append(segment)
                self.places[segment.place_id] = segment.place
                if segment.place_id in self.place_times:
                    self.place_times[segment.place_id]\
                            .append(segment.duration)
                else:
                    self.place_times[segment.place_id] =\
                            [segment.duration]

        for place_id, durations in self.place_times.iteritems():
            print self.places[place_id].get('name', None),\
                'Segments: ', len(durations),\
                'Total: ', reduce(operator.add, durations)


    def __iter__(self):
        for i in self.segments:
            yield i
