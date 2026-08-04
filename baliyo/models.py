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


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=255)
    phone_no = models.CharField(max_length=15)
    vendor_address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BillOfMaterial(models.Model):
    vendor = models.ForeignKey(
        "Vendor",
        on_delete=models.CASCADE,
        related_name="bill_of_materials",
        null=True,
        blank=True,
    )
    file = models.FileField(upload_to="bill_of_material/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file.name


class ProjectTool(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=255)
    quantity = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Component(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=255)
    vendor = models.ForeignKey(
        "Vendor",
        on_delete=models.CASCADE,
        related_name="components",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ComponentModel(models.Model):
    component = models.ForeignKey(
        "Component", on_delete=models.CASCADE, related_name="models"
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=255)
    specs = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ComponentPurchase(models.Model):
    vendor = models.ForeignKey(
        "Vendor",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="purchases",
    )
    purchase_date = models.DateField(null=True, blank=True)
    total_price = models.FloatField(null=True, blank=True, default=0.0)
    notes = models.TextField(null=True, blank=True)
    bill_file = models.FileField(
        upload_to="component_purchase_bills/", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["vendor", "purchase_date"]),
        ]

    def __str__(self):
        return f"Purchase #{self.id}" + (
            f" from {self.vendor.name}" if self.vendor else ""
        )


class ComponentPurchaseItem(models.Model):
    class UnitChoices(models.TextChoices):
        PCS = "pcs", "Pcs"
        KG = "kg", "Kg"
        METER = "m", "Meter"

    purchase = models.ForeignKey(
        ComponentPurchase,
        on_delete=models.CASCADE,
        related_name="items",
    )
    component_model = models.ForeignKey(
        "ComponentModel",
        on_delete=models.CASCADE,
        related_name="purchase_items",
    )
    quantity = models.IntegerField(default=1)
    unit = models.CharField(
        max_length=20,
        choices=UnitChoices.choices,
        default=UnitChoices.PCS,
    )
    price_per_item = models.FloatField(default=0.0)
    total_price = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} {self.unit} x {self.component_model.name} for Purchase #{self.purchase_id}"

    def save(self, *args, **kwargs):
        if self.quantity is not None and self.price_per_item is not None:
            self.total_price = float(self.quantity) * float(self.price_per_item)
        super().save(*args, **kwargs)


class Inventory(models.Model):
    component_model = models.ForeignKey(
        "ComponentModel",
        on_delete=models.CASCADE,
        related_name="inventory",
        null=True,
        blank=True,
    )
    quantity = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.component_model.name


class Project(models.Model):
    STATUS_CHOICES = (
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("published", "Published"),
    )
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default="in_progress", db_index=True
    )
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


class ProjectInventoryUsed(models.Model):
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="components_used"
    )
    inventory = models.ForeignKey(
        "Inventory", on_delete=models.CASCADE, related_name="projects_used"
    )
    quantity = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.project.title} - {self.inventory}"


class ProjectToolUsed(models.Model):
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="tools_used"
    )
    tool = models.ForeignKey(
        "ProjectTool", on_delete=models.CASCADE, related_name="projects_used"
    )
    quantity = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("project", "tool")
        indexes = [
            models.Index(fields=["project", "tool"]),
        ]

    def __str__(self):
        return f"{self.project.title} - {self.tool.name}"


class ProjectDemo(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    video_file = models.FileField(upload_to="project_demo/", null=True, blank=True)
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="demos"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TechnicalDocument(models.Model):
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="technical_document"
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(
        upload_to="project_technical_documents/", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProjectDailyUpdate(models.Model):
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="daily_updates"
    )
    task = models.TextField()
    decision = models.TextField(null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    problem = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.project.title} - {self.task[:30]}"


class ProjectOrder(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    project_name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project_name


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
