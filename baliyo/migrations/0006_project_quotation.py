# Generated by Django 5.1.5 on 2025-03-20 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baliyo', '0005_rename_service_project_category_project_catalogue_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='quotation',
            field=models.FileField(blank=True, null=True, upload_to='quotation/'),
        ),
    ]
