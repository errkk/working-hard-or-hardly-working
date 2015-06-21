# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('movesauth', '0004_auto_20150621_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 21, 14, 24, 54, 136398, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='token',
            name='redirect_uri',
            field=models.URLField(default='http://errkk.ngrok.io/movesauth/redirect'),
            preserve_default=False,
        ),
    ]
