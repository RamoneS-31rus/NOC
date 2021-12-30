# Generated by Django 3.2.4 on 2021-12-29 13:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gpon', '0003_alter_request_installer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='installer',
            field=models.ManyToManyField(blank=True, related_name='installer', to=settings.AUTH_USER_MODEL, verbose_name='Монтажники'),
        ),
    ]