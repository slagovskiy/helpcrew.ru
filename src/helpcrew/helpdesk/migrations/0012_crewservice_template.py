# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-28 04:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0011_auto_20170824_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='crewservice',
            name='template',
            field=models.TextField(default='', verbose_name='Шаблон заявки'),
        ),
    ]
