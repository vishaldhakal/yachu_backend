# Generated by Django 5.1.5 on 2025-03-20 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baliyo', '0006_project_quotation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='blogcategory',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
