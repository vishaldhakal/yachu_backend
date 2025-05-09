from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    ROLE_CHOICES = {
        ('Admin', 'Admin'),
        ('Customer', 'Customer'),
        ('Sales', 'Sales')
    }
    role = models.CharField(
        max_length=255, choices=ROLE_CHOICES, default='Customer')
    phone_number = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username
