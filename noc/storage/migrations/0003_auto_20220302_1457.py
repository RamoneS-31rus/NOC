# Generated by Django 3.2.4 on 2022-03-02 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0002_auto_20211202_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='income_date_create',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='income',
            name='income_date_update',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='object',
            name='date_create',
            field=models.DateField(auto_now_add=True),
        ),
    ]