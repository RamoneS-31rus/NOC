# Generated by Django 3.2.4 on 2022-02-09 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gpon', '0007_remove_house_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='request',
            options={'ordering': ['id']},
        ),
        migrations.AlterField(
            model_name='area',
            name='name',
            field=models.CharField(blank=True, max_length=50, unique=True),
        ),
    ]