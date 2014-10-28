# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_user_website'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='user_website',
            new_name='website',
        ),
    ]
