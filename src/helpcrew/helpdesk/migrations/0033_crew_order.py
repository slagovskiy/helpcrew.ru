# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-01 07:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0032_crewtask_date_work'),
    ]

    operations = [
        migrations.AddField(
            model_name='crew',
            name='order',
            field=models.IntegerField(default=10000, verbose_name='Определяет сортировку в списке команд'),
        ),
    ]