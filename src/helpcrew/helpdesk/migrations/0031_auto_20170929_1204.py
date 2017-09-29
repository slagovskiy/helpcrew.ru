# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-29 05:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('helpdesk', '0030_auto_20170928_1333'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(0, 'Наблюдатель'), (1, 'Дисптечер'), (2, 'Оператор'), (3, 'Ответственный')], default=0, verbose_name='Тип пользователя в рамках заявки')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='helpdesk.CrewTask', verbose_name='Заявка')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Участник заявки',
                'verbose_name_plural': 'Участники заявок',
                'ordering': ['task', 'user', 'type'],
            },
        ),
        migrations.AlterModelOptions(
            name='taskfiles',
            options={'verbose_name': 'Вложение к заявке', 'verbose_name_plural': 'Вложения к заявкам'},
        ),
    ]