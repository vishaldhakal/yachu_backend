# Generated by Django 4.1.4 on 2025-01-03 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cim', '0008_alter_thematicregistration_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='thematicsession',
            old_name='time',
            new_name='start_time',
        ),
        migrations.AddField(
            model_name='thematicsession',
            name='end_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]