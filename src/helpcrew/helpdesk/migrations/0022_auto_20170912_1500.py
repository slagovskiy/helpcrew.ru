# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-12 08:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0021_auto_20170912_1454'),
    ]

    operations = [
        migrations.RenameField(
            model_name='crew',
            old_name='launch_end_time',
            new_name='lunch_end_time',
        ),
        migrations.RenameField(
            model_name='crew',
            old_name='launch_start_time',
            new_name='lunch_start_time',
        ),
    ]
