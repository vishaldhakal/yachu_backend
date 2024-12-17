# Generated by Django 4.1.4 on 2024-12-17 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('Customer', 'Customer'), ('Sales', 'Sales'), ('Admin', 'Admin')], max_length=255),
        ),
    ]
