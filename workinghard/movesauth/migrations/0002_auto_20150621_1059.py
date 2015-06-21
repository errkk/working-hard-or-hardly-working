# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movesauth', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='token',
            old_name='moves_user_ud',
            new_name='moves_user_id',
        ),
    ]
