from django.db import models
from tinymce import models as tinymce_models


class Author(models.Model):
    name = models.CharField(max_length=200) 
    role = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    picture = models.FileField()
    about = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

class Category(models.Model):
    category_name = models.CharField(max_length=200, primary_key=True)
    category_image = models.FileField(blank=True)

    def __str__(self):
        return self.category_name

class Tag(models.Model):
    tag_name = models.CharField(max_length=200)

    def __str__(self):
        return self.tag_name


class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.CharField(max_length=300)
    title = models.CharField(max_length=500)
    blog_duration_to_read = models.CharField(max_length=100,blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    thumbnail_image = models.FileField()
    thumbnail_image_alt_description = models.CharField(max_length=300)
    blog_content = tinymce_models.HTMLField(blank=True)
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Event(models.Model):
    event_name = models.CharField(max_length=200)
    event_date = models.DateTimeField()
    event_location = models.CharField(max_length=200)
    event_description = tinymce_models.HTMLField(blank=True)
    event_image = models.FileField()
    event_image_alt_description = models.CharField(max_length=300)
    event_url = models.URLField()
    event_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    event_tags = models.ManyToManyField(Tag)
    event_author = models.ForeignKey(Author, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-event_date']

    def __str__(self):
        return self.event_name