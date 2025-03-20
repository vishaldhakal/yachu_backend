# Generated by Django 5.1.5 on 2025-03-20 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baliyo', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='project_name',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='service',
            old_name='service_name',
            new_name='title',
        ),
        migrations.AlterField(
            model_name='blog',
            name='slug',
            field=models.SlugField(),
        ),
        migrations.AlterField(
            model_name='blog',
            name='thumbnail_image',
            field=models.FileField(blank=True, null=True, upload_to='blog/'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='thumbnail_image_alt_description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(),
        ),
        migrations.AlterField(
            model_name='service',
            name='slug',
            field=models.SlugField(),
        ),
    ]
