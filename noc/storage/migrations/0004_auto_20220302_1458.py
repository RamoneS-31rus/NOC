# Generated by Django 3.2.4 on 2022-03-02 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0003_auto_20220302_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='income_date_create',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='income',
            name='income_date_update',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
