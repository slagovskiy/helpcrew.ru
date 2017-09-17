# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-17 09:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dyntable', '0003_field'),
    ]

    operations = [
        migrations.CreateModel(
            name='Index',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(default=0, verbose_name='Номер строки')),
                ('deleted', models.BooleanField(default=False, verbose_name='Строка удалена')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dyntable.Table', verbose_name='Таблица')),
            ],
            options={
                'verbose_name': 'Номер строки',
                'verbose_name_plural': 'Номера строк',
                'ordering': ['table', 'num'],
            },
        ),
    ]
