# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movesauth', '0005_auto_20150621_1425'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='token',
            name='redirect_uri',
        ),
    ]
