# Generated by Django 5.1.5 on 2025-04-04 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baliyo', '0013_remove_image_alt_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='icon',
            field=models.FileField(blank=True, null=True, upload_to='icon/'),
        ),
        migrations.AddField(
            model_name='service',
            name='short_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
