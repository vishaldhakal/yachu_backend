from django.db import models
from about.models import Franchise
# Create your models here.


class Contact(models.Model):
    franchise = models.ForeignKey(
        Franchise, on_delete=models.CASCADE, blank=True, null=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
