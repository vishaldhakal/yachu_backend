from django.db import models
from tinymce import models as tinymce_models

class Franchise(models.Model):
    franchise_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=200)
    description = tinymce_models.HTMLField(blank=True)
    address = models.TextField(max_length=500)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.FileField(blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name