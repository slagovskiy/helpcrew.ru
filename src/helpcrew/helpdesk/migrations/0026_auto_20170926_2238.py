# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-26 15:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0025_crew_avatar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='crew',
            old_name='avatar',
            new_name='logo',
        ),
    ]