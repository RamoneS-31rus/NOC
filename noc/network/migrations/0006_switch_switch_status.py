# Generated by Django 3.2 on 2021-04-23 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_alter_vlanhistory_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='switch',
            name='switch_status',
            field=models.BooleanField(default=False),
        ),
    ]
