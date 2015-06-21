from django.db import models
from django.conf import settings


class Token(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    access_token = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=200)
    moves_user_id = models.BigIntegerField()
    expires = models.DateTimeField()

    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return 'Token for: {0}'.format(self.user.username)
