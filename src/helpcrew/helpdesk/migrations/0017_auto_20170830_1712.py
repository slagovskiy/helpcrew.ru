# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-30 10:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0016_auto_20170830_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crewtask',
            name='date_close',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата закрытия заявки'),
        ),
        migrations.AlterField(
            model_name='crewtask',
            name='date_end',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата окончания подписки'),
        ),
        migrations.AlterField(
            model_name='crewtask',
            name='date_finish',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата выполнения заявки'),
        ),
        migrations.AlterField(
            model_name='crewtask',
            name='date_in',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата подачи заявки'),
        ),
        migrations.AlterField(
            model_name='crewusers',
            name='type',
            field=models.IntegerField(choices=[(0, 'Administrator'), (1, 'Dispatcher'), (2, 'Operator'), (3, 'Observer')], default=2, verbose_name='Уровеь доступа'),
        ),
    ]
