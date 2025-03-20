# Generated by Django 5.1.5 on 2025-03-17 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0058_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('Customer', 'Customer'), ('Sales', 'Sales'), ('Admin', 'Admin')], max_length=255),
        ),
    ]
