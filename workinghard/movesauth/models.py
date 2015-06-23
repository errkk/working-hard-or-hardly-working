from datetime import datetime

import requests

from django.utils import timezone
from django.db import models
from django.conf import settings

from .movesclient import Moves

moves = Moves(settings.MOVES_CLIENT_ID,
              settings.MOVES_CLIENT_SECRET)


class Token(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    access_token = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=200)
    moves_user_id = models.BigIntegerField()
    expires = models.DateTimeField()

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return 'Token for: {0}'.format(self.user.username)

    def has_expired(self):
        return self.expires < timezone.now()

    def refresh(self):
        res, expires = moves.refresh_token(self.refresh_token)

        if res['access_token']:
            self.access_token = res['access_token']
            self.refresh_token = res['refresh_token']
            self.expires = expires
            self.save(update_fields=['access_token',
                                     'refresh_token',
                                     'expires'])

    def query(self, endpoint, **kwargs):
        headers = {
            'Authorization': 'Bearer {0}'.format(self.access_token),
        }
        res = requests.get(Moves.BASE_URI + endpoint,
                           params=kwargs, headers=headers)
        return res.json()


class UserData(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    workplace_id = models.IntegerField(blank=True, null=True)
    workplace_name = models.CharField(max_length=100, blank=True,
                                      null=True)

    def __unicode__(self):
        return '<{0} @ {1}>'.format(self.user.username,
                                    self.workplace_name)
