# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-03 05:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userext', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='firstname',
            field=models.CharField(blank=True, default='', max_length=40, null=True, verbose_name='First name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='lastname',
            field=models.CharField(blank=True, default='', max_length=40, null=True, verbose_name='Last name'),
        ),
    ]
