# Generated by Django 3.2.4 on 2021-12-22 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('addressbook', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='slug',
        ),
    ]
