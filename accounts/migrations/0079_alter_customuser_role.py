# Generated by Django 5.1.5 on 2025-03-20 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0078_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('Customer', 'Customer'), ('Admin', 'Admin'), ('Sales', 'Sales')], default='Customer', max_length=255),
        ),
    ]
