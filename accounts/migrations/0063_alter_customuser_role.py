# Generated by Django 5.1.5 on 2025-03-20 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0062_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Customer', 'Customer'), ('Sales', 'Sales')], max_length=255),
        ),
    ]
