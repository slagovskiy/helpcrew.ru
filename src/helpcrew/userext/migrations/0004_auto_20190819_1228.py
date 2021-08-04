# Generated by Django 2.2.3 on 2019-08-19 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userext', '0003_user_interface_wide_screen'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password_request_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='password change request timeout'),
        ),
        migrations.AddField(
            model_name='user',
            name='password_request_token',
            field=models.CharField(blank=True, default='', max_length=40, null=True, verbose_name='password change request token'),
        ),
    ]