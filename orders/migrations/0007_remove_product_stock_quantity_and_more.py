# Generated by Django 5.1.5 on 2025-03-26 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_remove_order_city_remove_order_landmark_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='stock_quantity',
        ),
        migrations.AlterField(
            model_name='order',
            name='alternate_phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
