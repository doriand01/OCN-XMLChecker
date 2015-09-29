# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('xmlchecker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='errors',
            name='errors_es',
            field=models.TextField(default='es'),
            preserve_default=False,
        ),
    ]
