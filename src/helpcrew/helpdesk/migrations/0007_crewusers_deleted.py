# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-18 07:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0006_auto_20170815_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='crewusers',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='Член команды удален'),
        ),
    ]
