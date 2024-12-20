# Generated by Django 4.1.4 on 2024-12-17 14:17

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(default=django.utils.timezone.now)),
                ('venue', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField(default=django.utils.timezone.now)),
                ('end_time', models.TimeField(default=django.utils.timezone.now)),
                ('max_participants', models.IntegerField(default=0)),
                ('current_participants', models.IntegerField(default=0)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_slots', to='rojgar_pavillion.topic')),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_type', models.CharField(choices=[('SINGLE', 'Single Person'), ('GROUP', 'Group'), ('EXPO_ACCESS', 'Expo Access')], max_length=20)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('CONFIRMED', 'Confirmed'), ('CANCELLED', 'Cancelled')], default='PENDING', max_length=20)),
                ('full_name', models.CharField(max_length=200)),
                ('qualification', models.CharField(choices=[('Under SEE', 'Under SEE'), ('10+2', '10+2'), ('Graduate', 'Graduate'), ('Post Graduate', 'Post Graduate')], max_length=20)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10)),
                ('age', models.IntegerField(validators=[django.core.validators.MinValueValidator(14)])),
                ('address', models.TextField()),
                ('mobile_number', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'", regex='^\\+?1?\\d{9,15}$')])),
                ('email', models.EmailField(max_length=254)),
                ('total_participants', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('payment_method', models.CharField(choices=[('Nabil_Bank', 'Nabil Bank')], max_length=20)),
                ('payment_screenshot', models.ImageField(blank=True, null=True, upload_to='payments/')),
                ('agreed_to_no_refund', models.BooleanField(default=False)),
                ('is_early_bird', models.BooleanField(default=False)),
                ('is_expo_access', models.BooleanField(default=False)),
                ('is_free_entry', models.BooleanField(default=False)),
                ('qr_code', models.ImageField(blank=True, null=True, upload_to='qr_codes/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('time_slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rojgar_pavillion.timeslot')),
            ],
        ),
    ]
