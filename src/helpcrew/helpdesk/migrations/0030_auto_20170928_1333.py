# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-28 06:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0029_crew_is_public'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crewtask',
            name='dispatcher_close',
        ),
        migrations.RemoveField(
            model_name='crewtask',
            name='dispatcher_in',
        ),
        migrations.RemoveField(
            model_name='crewtask',
            name='observer',
        ),
        migrations.RemoveField(
            model_name='crewtask',
            name='operator',
        ),
    ]
