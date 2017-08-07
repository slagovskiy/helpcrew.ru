# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-07 06:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0004_auto_20170807_1241'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServicePrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Дата начала тействия цены')),
                ('cost', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Стоимость услуги')),
                ('prepay', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Предоплата')),
                ('fine1', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Штраф за невыполнение заявки в срок')),
                ('fine2', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Штраф за просроченную заявку')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='helpdesk.CrewService', verbose_name='Услуга')),
            ],
            options={
                'verbose_name': 'Строимость услуги',
                'verbose_name_plural': 'Стоимость услуг',
                'ordering': ['service', 'start_date'],
            },
        ),
        migrations.AlterModelOptions(
            name='crew',
            options={'ordering': ['name'], 'verbose_name': 'Команда', 'verbose_name_plural': 'Команды'},
        ),
        migrations.AlterModelOptions(
            name='crewusers',
            options={'ordering': ['type', 'user'], 'verbose_name': 'Член команды', 'verbose_name_plural': 'Члены команд'},
        ),
    ]