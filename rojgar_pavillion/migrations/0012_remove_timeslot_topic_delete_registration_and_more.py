# Generated by Django 5.1.5 on 2025-03-20 08:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rojgar_pavillion', '0011_registration_is_attended'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timeslot',
            name='topic',
        ),
        migrations.DeleteModel(
            name='Registration',
        ),
        migrations.DeleteModel(
            name='TimeSlot',
        ),
        migrations.DeleteModel(
            name='Topic',
        ),
    ]
