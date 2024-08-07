# Generated by Django 4.1.4 on 2024-07-20 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StallBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('chief_executive', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('stall_type', models.CharField(choices=[('National Prime', 'National Prime'), ('National General', 'National General'), ('International', 'International'), ('Agro & MSME', 'Agro & MSME'), ('Automobiles', 'Automobiles'), ('Food Stalls', 'Food Stalls'), ('BDS Providers', 'BDS Providers')], max_length=200)),
                ('stall_no', models.CharField(max_length=200)),
                ('merge_or_separate', models.CharField(choices=[('MERGE', 'Merge'), ('SEPARATE', 'Separate')], max_length=100)),
                ('voucher', models.FileField(upload_to='vouchers/')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('advance_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('remaining_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('amount_in_words', models.TextField()),
                ('terms_and_conditions_accepted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Stall Booking',
                'verbose_name_plural': 'Stall Bookings',
            },
        ),
    ]
