# Generated by Django 4.1.4 on 2025-01-10 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cim', '0012_remove_thematicregistration_hotel_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thematicregistration',
            name='hotel',
            field=models.CharField(blank=True, max_length=220, null=True),
        ),
    ]
