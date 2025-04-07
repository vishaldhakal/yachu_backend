from django.db import models
from django.utils.text import slugify

# Create your models here.


class Service(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=255)
    description = models.TextField()
    short_description = models.TextField(null=True, blank=True)
    icon = models.FileField(upload_to='icon/', null=True, blank=True)
    thumbnail_image = models.FileField(
        upload_to='service/', null=True, blank=True)
    thumbnail_image_alt_description = models.CharField(
        max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Image(models.Model):
    image = models.FileField(upload_to='images/')
    project = models.ForeignKey(
        'Project', on_delete=models.CASCADE, related_name='images')


class Project(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=255)
    category = models.ManyToManyField(
        'Service', related_name='projects', blank=True)
    description = models.TextField()
    meta_title = models.CharField(max_length=255, null=True, blank=True)
    meta_description = models.CharField(max_length=255, null=True, blank=True)
    thumbnail_image = models.FileField(
        upload_to='project/', null=True, blank=True)
    thumbnail_image_alt_description = models.CharField(
        max_length=255, null=True, blank=True)
    catalogue = models.FileField(upload_to='catalogue/', null=True, blank=True)
    quotation = models.FileField(upload_to='quotation/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class OurPartner(models.Model):
    title = models.CharField(max_length=255)
    image = models.FileField(upload_to='our_partner/', null=True, blank=True)
    image_alt_description = models.CharField(
        max_length=255, null=True, blank=True)
    website_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class BlogCategory(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class BlogTag(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Blog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=255)
    description = models.TextField()
    meta_title = models.CharField(max_length=255, null=True, blank=True)
    meta_description = models.CharField(max_length=255, null=True, blank=True)
    thumbnail_image = models.FileField(
        upload_to='blog/', null=True, blank=True)
    thumbnail_image_alt_description = models.CharField(
        max_length=255, null=True, blank=True)
    category = models.ForeignKey(
        'BlogCategory', on_delete=models.CASCADE, related_name='blogs')
    tags = models.ManyToManyField('BlogTag', related_name='blogs', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TeamMember(models.Model):
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255, null=True, blank=True)
    image = models.FileField(upload_to='team/', null=True, blank=True)
    image_alt_description = models.CharField(
        max_length=255, null=True, blank=True)
    department = models.ForeignKey(
        'Department', on_delete=models.CASCADE, related_name='team_members', blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Faq(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question


class Testimonial(models.Model):
    name = models.CharField(max_length=255)
    message = models.TextField()
    rating = models.IntegerField()
    designation = models.CharField(max_length=255, null=True, blank=True)
    image = models.FileField(upload_to='testimonial/', null=True, blank=True)
    image_alt_description = models.CharField(
        max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Gallery(models.Model):
    CHOICES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )
    title = models.CharField(max_length=255)
    media = models.FileField(upload_to='image_gallery/', null=True, blank=True)
    media_type = models.CharField(
        max_length=255, choices=CHOICES, null=True, blank=True)
    media_alt_description = models.CharField(
        max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
