# Generated by Django 4.1.4 on 2024-07-20 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cim', '0002_alter_stallbooking_merge_or_separate'),
    ]

    operations = [
        migrations.AddField(
            model_name='stallbooking',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=100),
        ),
    ]
