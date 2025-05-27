from django.db import models
from accounts.models import Organization
from accounts.models import Department
# Create your models here.


class FinanceRecord(models.Model):
    TRANSACTION_TYPE = [
        ('Receivable', 'Receivable'),
        ('Payable', 'Payable'),
        ('Received', 'Received'),
        ('Paid', 'Paid'),
    ]
    PAYMENT_METHOD = [
        ('Cash', 'Cash'),
        ('Bank', 'Bank')
    ]

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    transaction_type = models.CharField(
        max_length=10, choices=TRANSACTION_TYPE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=True, blank=True)
    payment_method = models.CharField(
        max_length=10, choices=PAYMENT_METHOD, null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.transaction_type} - {self.amount}'


class Stock(models.Model):
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, null=True, blank=True)
    product_name = models.CharField(max_length=100)
    product_code = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product} - {self.quantity}'
