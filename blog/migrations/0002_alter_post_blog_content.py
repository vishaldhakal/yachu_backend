# Generated by Django 4.1.4 on 2024-05-07 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='blog_content',
            field=models.TextField(blank=True),
        ),
    ]