# Generated by Django 4.1.4 on 2024-10-26 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('Customer', 'Customer'), ('Sales', 'Sales'), ('Admin', 'Admin')], max_length=255),
        ),
    ]
