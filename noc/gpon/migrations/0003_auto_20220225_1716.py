# Generated by Django 3.2.4 on 2022-02-25 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gpon', '0002_request_whose_cord'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='time',
        ),
        migrations.RemoveField(
            model_name='request',
            name='user',
        ),
        migrations.AlterField(
            model_name='request',
            name='whose_cord',
            field=models.BooleanField(default=False, verbose_name='Абонентский'),
        ),
    ]