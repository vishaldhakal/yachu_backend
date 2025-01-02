# Generated by Django 4.1.4 on 2025-01-02 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('Customer', 'Customer'), ('Sales', 'Sales'), ('Admin', 'Admin')], max_length=255),
        ),
    ]
