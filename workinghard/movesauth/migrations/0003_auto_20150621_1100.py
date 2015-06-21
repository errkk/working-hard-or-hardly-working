# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movesauth', '0002_auto_20150621_1059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='moves_user_id',
            field=models.BigIntegerField(),
        ),
    ]
