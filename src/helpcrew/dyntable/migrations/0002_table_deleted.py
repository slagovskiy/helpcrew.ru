# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-04 15:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dyntable', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name='Запись удалена'),
        ),
    ]