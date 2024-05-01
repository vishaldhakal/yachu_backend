# Generated by Django 4.1.4 on 2024-05-01 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_rename_avatar_testimonial_after_testimonial_before'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileSchema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='FormData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=100)),
                ('team_description', models.TextField()),
                ('robot_name', models.CharField(max_length=100)),
                ('robot_description', models.TextField()),
                ('members', models.ManyToManyField(related_name='form_data', to='home.member')),
                ('robot_photos', models.ManyToManyField(blank=True, related_name='form_data', to='home.fileschema')),
            ],
        ),
    ]
