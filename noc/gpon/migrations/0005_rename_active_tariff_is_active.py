# Generated by Django 3.2.4 on 2022-03-31 08:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gpon', '0004_auto_20220316_1709'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tariff',
            old_name='active',
            new_name='is_active',
        ),
    ]