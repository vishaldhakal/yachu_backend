# Generated by Django 4.1.4 on 2024-12-19 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rojgar_pavillion', '0004_registration_group_members_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='payment_screenshot',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
