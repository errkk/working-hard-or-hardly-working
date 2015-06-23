# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movesauth', '0007_userdata'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userdata',
            old_name='workplace',
            new_name='workplace_name',
        ),
        migrations.AddField(
            model_name='userdata',
            name='workplace_id',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
