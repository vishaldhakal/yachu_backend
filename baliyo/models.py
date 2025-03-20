from django.db import models
from django.utils.text import slugify

# Create your models here.
class SlugMixin:
    
    def generate_unique_slug(self):
        self.slug = slugify(self.title)

    def save(self, *args, **kwargs):
        self.generate_unique_slug()
        super().save(*args, **kwargs)

class Service(models.Model,SlugMixin):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    thumbnail_image = models.FileField(upload_to='service/',null=True,blank=True)
    thumbnail_image_alt_description = models.CharField(max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Image(models.Model):
    image=models.FileField(upload_to='images/')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='images')

class Project(models.Model,SlugMixin):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    category = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='projects')
    description = models.TextField()
    meta_title = models.CharField(max_length=255,null=True,blank=True)
    meta_description = models.CharField(max_length=255,null=True,blank=True)
    thumbnail_image = models.FileField(upload_to='project/',null=True,blank=True)
    thumbnail_image_alt_description = models.CharField(max_length=255,null=True,blank=True)
    catalogue=models.FileField(upload_to='catalogue/',null=True,blank=True)
    quotation=models.FileField(upload_to='quotation/',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class BlogCategory(models.Model,SlugMixin):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class BlogTag(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Blog(models.Model,SlugMixin):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    thumbnail_image = models.FileField(upload_to='blog/',null=True,blank=True)
    thumbnail_image_alt_description = models.CharField(max_length=255,null=True,blank=True)
    category = models.ForeignKey('BlogCategory', on_delete=models.CASCADE, related_name='blogs')
    tags = models.ManyToManyField('BlogTag', related_name='blogs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Contact(models.Model):
    name=models.CharField(max_length=255)
    email=models.EmailField()
    phone=models.CharField(max_length=255)
    message=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class TeamMember(models.Model):
    name=models.CharField(max_length=255)
    designation=models.CharField(max_length=255)
    image=models.FileField(upload_to='team/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Faq(models.Model):
    question=models.CharField(max_length=255)
    answer=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

class Testimonial(models.Model):
    name=models.CharField(max_length=255)
    message=models.TextField()
    rating=models.IntegerField()
    designation=models.CharField(max_length=255,null=True,blank=True)
    image=models.FileField(upload_to='testimonial/',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


