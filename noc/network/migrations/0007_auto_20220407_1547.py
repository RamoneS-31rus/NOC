# Generated by Django 3.2.4 on 2022-04-07 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_switch_switch_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='switch',
            old_name='switch_address',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='switch',
            old_name='switch_firmware',
            new_name='firmware',
        ),
        migrations.RenameField(
            model_name='switch',
            old_name='switch_ip',
            new_name='ip',
        ),
        migrations.RenameField(
            model_name='switch',
            old_name='switch_mac',
            new_name='mac',
        ),
        migrations.RenameField(
            model_name='switch',
            old_name='switch_model',
            new_name='model',
        ),
        migrations.RenameField(
            model_name='switch',
            old_name='switch_note',
            new_name='note',
        ),
        migrations.RenameField(
            model_name='switch',
            old_name='switch_order',
            new_name='order',
        ),
        migrations.RenameField(
            model_name='switch',
            old_name='switch_serial',
            new_name='serial',
        ),
        migrations.RenameField(
            model_name='switch',
            old_name='switch_status',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='switch',
            old_name='switch_time',
            new_name='time',
        ),
        migrations.RenameField(
            model_name='switch',
            old_name='switch_user',
            new_name='user',
        ),
    ]
