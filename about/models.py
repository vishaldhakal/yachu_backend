from django.db import models
from tinymce import models as tinymce_models
from django.utils.text import slugify


class Franchise(models.Model):
    franchise_name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    description = tinymce_models.HTMLField(blank=True)
    address = models.TextField(max_length=500, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    image = models.FileField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.franchise_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.franchise_name)
        super().save(*args, **kwargs)
