# Generated by Django 5.1.5 on 2025-01-23 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cim', '0022_alter_panelist_sub_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='panelist',
            name='sub_session',
            field=models.ManyToManyField(blank=True, related_name='panelists', to='cim.subsession'),
        ),
    ]
