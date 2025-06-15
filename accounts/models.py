from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
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
    person_in_charge = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    opening_balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    vat_number = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Project(models.Model):
    organization = models.ForeignKey(
        "Organization", on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class ProjectNotes(models.Model):
    user = models.ForeignKey(
        "CustomUser", on_delete=models.CASCADE, related_name='notes')
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name='notes')
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.notes

class ProjectReminder(models.Model):
    TYPE = [
        ('Task', 'Task'),
        ('Meeting', 'Meeting'),
        ('Event', 'Event'),
        ('Follow Up', 'Follow Up'),
        ('Call', 'Call'),
    ]
    user = models.ForeignKey(
        "CustomUser", on_delete=models.CASCADE, related_name='reminders')
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name='reminders')
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=10, choices=TYPE, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title


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
