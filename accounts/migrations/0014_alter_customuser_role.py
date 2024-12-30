# Generated by Django 4.1.4 on 2024-12-30 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('Customer', 'Customer'), ('Admin', 'Admin'), ('Sales', 'Sales')], max_length=255),
        ),
    ]