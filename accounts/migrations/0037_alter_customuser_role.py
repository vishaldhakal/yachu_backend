# Generated by Django 4.1.4 on 2025-01-13 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0036_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('Sales', 'Sales'), ('Admin', 'Admin'), ('Customer', 'Customer')], max_length=255),
        ),
    ]
