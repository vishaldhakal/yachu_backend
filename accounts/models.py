from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class OrganizationContacts(models.Model):
    organization = models.ForeignKey(
        "Organization", on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(null=True, blank=True)
    position = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Organization(models.Model):
    name = models.CharField(max_length=100)
    person_in_charge = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    opening_balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    address = models.CharField(max_length=255, null=True, blank=True)
    vat_number = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    opening_balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.FileField(
        upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return self.user.username
