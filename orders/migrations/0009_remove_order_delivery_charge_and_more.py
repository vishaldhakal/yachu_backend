# Generated by Django 5.1.5 on 2025-03-26 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_alter_orderproduct_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='delivery_charge',
        ),
        migrations.RemoveField(
            model_name='order',
            name='payment_method',
        ),
        migrations.RemoveField(
            model_name='order',
            name='payment_screenshot',
        ),
    ]
