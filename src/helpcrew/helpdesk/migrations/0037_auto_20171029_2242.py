# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-29 15:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0036_auto_20171029_2229'),
    ]

    operations = [
        migrations.AddField(
            model_name='crewusers',
            name='task_filter',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='crewusers',
            name='task_page_size',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='crewusers',
            name='task_paging',
            field=models.BooleanField(default=True),
        ),
    ]
