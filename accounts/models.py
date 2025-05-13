from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Organization(models.Model):
    TRANSACTION_TYPE = [
        ('RECEIVABLE', 'Receivable'),
        ('PAYABLE', 'Payable'),
    ]
    name = models.CharField(max_length=100)
    person_in_charge = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    transaction_type = models.CharField(
        max_length=10, choices=TRANSACTION_TYPE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.user.username
