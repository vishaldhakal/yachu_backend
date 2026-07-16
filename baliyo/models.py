import os

import resend
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.text import slugify

# from dotenv import load_dotenv

# load_dotenv()
# Create your models here.


class Service(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=255)
    description = models.TextField()
    short_description = models.TextField(null=True, blank=True)
    icon = models.FileField(upload_to="icon/", null=True, blank=True)
    thumbnail_image = models.FileField(upload_to="service/", null=True, blank=True)
    thumbnail_image_alt_description = models.CharField(
        max_length=255, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Image(models.Model):
    image = models.FileField(upload_to="images/")
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="images"
    )

    def __str__(self):
        return self.project.title


class Project(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=255)
    category = models.ManyToManyField("Service", related_name="projects", blank=True)
    description = models.TextField(null=True, blank=True)
    specs = models.TextField(null=True, blank=True)
    problem_it_solves = models.TextField(null=True, blank=True)
    case_study = models.TextField(null=True, blank=True)
    thumbnail_image = models.FileField(upload_to="project/", null=True, blank=True)
    thumbnail_image_alt_description = models.CharField(
        max_length=255, null=True, blank=True
    )
    team_member = models.TextField(null=True, blank=True)
    catalogue = models.FileField(upload_to="catalogue/", null=True, blank=True)
    quotation = models.FileField(upload_to="quotation/", null=True, blank=True)
    meta_title = models.CharField(max_length=255, null=True, blank=True)
    meta_description = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ProjectDemo(models.Model):
    video_url = models.URLField(null=True, blank=True)
    video_file = models.FileField(upload_to="project_demo/", null=True, blank=True)
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="demos"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project.title


class ProjectRenderingImage(models.Model):
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="rendering_images"
    )
    image = models.FileField(
        upload_to="project_rendering_image/", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project.title


class OurPartner(models.Model):
    title = models.CharField(max_length=255)
    image = models.FileField(upload_to="our_partner/", null=True, blank=True)
    image_alt_description = models.CharField(max_length=255, null=True, blank=True)
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
    thumbnail_image = models.FileField(upload_to="blog/", null=True, blank=True)
    thumbnail_image_alt_description = models.CharField(
        max_length=255, null=True, blank=True
    )
    category = models.ForeignKey(
        "BlogCategory", on_delete=models.CASCADE, related_name="blogs"
    )
    tags = models.ManyToManyField("BlogTag", related_name="blogs", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Contact(models.Model):
    CHOICES = (
        ("baliyoventures", "baliyoventures"),
        ("baliyotechnologies", "baliyotechnologies"),
    )
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=255)
    company = models.CharField(
        max_length=255,
        choices=CHOICES,
        default="baliyoventures",
    )
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
    image = models.FileField(upload_to="team/", null=True, blank=True)
    image_alt_description = models.CharField(max_length=255, null=True, blank=True)
    department = models.ForeignKey(
        "Department",
        on_delete=models.CASCADE,
        related_name="team_members",
        blank=True,
        null=True,
    )
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
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
    image = models.FileField(upload_to="testimonial/", null=True, blank=True)
    image_alt_description = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Gallery(models.Model):
    CHOICES = (
        ("image", "Image"),
        ("video", "Video"),
    )
    title = models.CharField(max_length=255)
    media = models.FileField(upload_to="image_gallery/", null=True, blank=True)
    media_type = models.CharField(
        max_length=255, choices=CHOICES, null=True, blank=True
    )
    media_alt_description = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class LeaveForm(models.Model):
    CHOICES = (
        ("paid", "Paid"),
        ("sick", "Sick"),
        ("unpaid", "Unpaid"),
        ("weekly", "Weekly"),
        ("other", "Other"),
    )
    APPROVED_BY_CHOICES = (
        ("Anil Singh", "Anil Singh"),
        ("Prithvi Chaudhary", "Prithvi Chaudhary"),
        ("Manav Khadka", "Manav Khadka"),
        ("Sapana Dhakal", "Sapana Dhakal"),
    )
    employee_name = models.CharField(max_length=255)
    employee_contact_number = models.CharField(max_length=255)
    employee_email = models.CharField(max_length=255)
    reason_of_leave = models.CharField(max_length=255, choices=CHOICES)
    brief_reason = models.TextField()
    days = models.IntegerField()
    leave_from_date = models.DateField()
    leave_to_date = models.DateField()
    approved_by = models.CharField(max_length=255, choices=APPROVED_BY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.employee_name

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            try:
                resend.api_key = os.getenv("RESEND_API_KEY")

                # Get current date and time
                now = timezone.localtime(timezone.now())
                context = {
                    "employee_name": self.employee_name,
                    "employee_email": self.employee_email,
                    "employee_contact_number": self.employee_contact_number,
                    "reason_of_leave": self.reason_of_leave,
                    "brief_reason": self.brief_reason,
                    "days": self.days,
                    "leave_from_date": self.leave_from_date.strftime("%B %d, %Y")
                    if self.leave_from_date
                    else "",
                    "leave_to_date": self.leave_to_date.strftime("%B %d, %Y")
                    if self.leave_to_date
                    else "",
                    "approved_by": self.approved_by,
                    "date": now.strftime("%B %d, %Y"),
                    "time": now.strftime("%I:%M %p"),
                }

                html_message = render_to_string(
                    "emails/leave_notification.html", context
                )

                params = {
                    "from": "Baliyo Leave Form <contact@baliyoventures.com>",
                    "to": [
                        "baliyoventures@gmail.com",
                        "baliyotechnologies@gmail.com",
                        "sapanachaudhary456@gmail.com",
                        "sapanadhakal.00@gmail.com",
                    ],
                    "subject": f"New Leave Request from {self.employee_name}",
                    "html": html_message,
                    "reply_to": self.employee_email,
                }

                resend.Emails.send(params)
            except Exception as e:
                # Log the error so database save is not blocked if email sending fails
                print(f"Error sending leave notification email: {str(e)}")
