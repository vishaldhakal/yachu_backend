# Generated by Django 4.1.4 on 2024-12-29 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Sales', 'Sales'), ('Customer', 'Customer')], max_length=255),
        ),
    ]