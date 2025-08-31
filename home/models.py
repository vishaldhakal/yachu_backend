from django.db import models
from solo.models import SingletonModel
from tinymce import models as tinymce_models
from about.models import Franchise
from django.utils.text import slugify


class SiteConfiguration(SingletonModel):
    meta_title = models.CharField(
        max_length=200, default="Meta Title Landing Page")
    meta_description = models.TextField(
        default="Meta Description Landing Page")
    hero_title = models.CharField(max_length=328, default="Title")
    hero_section_subtitle = models.TextField(
        default="Discover The Best Hiking Trails And Bee-Watching Spots On Your Next Adventure. Book A Trip Now")
    hero_section_image = models.FileField(blank=True)
    about_founder = tinymce_models.HTMLField(blank=True)
    message_from_ceo = tinymce_models.HTMLField(blank=True)
    our_story = tinymce_models.HTMLField(blank=True)

    def __str__(self):
        return "Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"


class FAQCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class FAQ(models.Model):
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE)
    question = models.TextField(max_length=500)
    answer = models.TextField(max_length=1000)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question


class Department(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class TeamMember(models.Model):
    franchise = models.ForeignKey(
        Franchise, on_delete=models.CASCADE, blank=True, null=True)
    order = models.IntegerField(blank=True)
    name = models.CharField(max_length=200, blank=True)
    role = models.CharField(max_length=200, blank=True)
    photo = models.FileField(blank=True, null=True)
    about = tinymce_models.HTMLField(blank=True)
    department = models.ForeignKey(
        Department, on_delete=models.DO_NOTHING, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    facebook = models.URLField(max_length=200, blank=True, null=True)
    instagram = models.URLField(max_length=200, blank=True, null=True)
    linkedin = models.URLField(max_length=200, blank=True, null=True)
    twitter = models.URLField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ('order', 'name',)


class Testimonial(models.Model):

    SOURCE_CHOICES = (
        ("In Person", "In Person"),
        ("Facebook", "Facebook"),
        ("Google", "Google"),
        ("Others", "Others"),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200, blank=True)
    before = models.FileField(blank=True)
    after = models.FileField(blank=True)
    role = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=500, blank=True)
    source = models.CharField(
        max_length=200, choices=SOURCE_CHOICES, default="Others")
    review = models.TextField(blank=True)
    rating = models.FloatField(default=5)

    def __str__(self) -> str:
        return self.name


class Banners(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    image = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ImageGallery(models.Model):
    title = models.CharField(max_length=200)
    image = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class VideoGallery(models.Model):
    title = models.CharField(max_length=200)
    youtube_video_link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    description = tinymce_models.HTMLField(blank=True)
    order = models.IntegerField(null=True, blank=True)
    price = models.FloatField()
    image1 = models.FileField()
    image2 = models.FileField(blank=True, null=True)
    image3 = models.FileField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ('order', 'title',)


class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()


class FormData(models.Model):
    team_name = models.CharField(max_length=100)
    team_description = models.TextField()
    members = models.ManyToManyField(Member, related_name='form_data')
    robot_name = models.CharField(max_length=100)
    robot_description = models.TextField()
    robot_photos = models.ManyToManyField(
        'FileSchema', related_name='form_data', blank=True)


class FileSchema(models.Model):
    file = models.FileField(upload_to='uploads/')
