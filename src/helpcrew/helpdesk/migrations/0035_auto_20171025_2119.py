# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-25 14:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0034_auto_20171002_2305'),
    ]

    operations = [
        migrations.AddField(
            model_name='crewusers',
            name='dtable_filter',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='crewusers',
            name='dtable_page_size',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='crewusers',
            name='dtable_paging',
            field=models.BooleanField(default=True),
        ),
    ]
