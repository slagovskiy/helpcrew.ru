# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-04 05:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0018_auto_20170904_1135'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crew',
            name='launch_days',
        ),
    ]