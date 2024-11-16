from django.db import models
from django.core.validators import EmailValidator, RegexValidator
from django.utils.text import slugify

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class ServiceCategory(BaseModel):
    name = models.CharField(
        max_length=255, 
        unique=True,
        help_text="Name of the service category"
    )
    description = models.TextField(help_text="Detailed description of the category")

    class Meta:
        verbose_name_plural = "Service Categories"
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name

class ServiceSubCategory(BaseModel):
    category = models.ForeignKey(
        ServiceCategory, 
        on_delete=models.CASCADE, 
        related_name='subcategories',
        db_index=True
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    class Meta:
        verbose_name_plural = "Service Sub Categories"
        unique_together = ['category', 'name']
        ordering = ['category', 'name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category', 'name']),
        ]

    

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class NtcService(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(
        ServiceCategory, 
        on_delete=models.CASCADE, 
        related_name='services'
    )
    subcategory = models.ForeignKey(
        ServiceSubCategory, 
        on_delete=models.CASCADE, 
        related_name='services'
    )
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category', 'subcategory']),
        ]

    

    def __str__(self):
        return self.name

class NtcPackage(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    services = models.ForeignKey(NtcService,on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name



class NtcCustomerCare(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    contact = models.CharField(
        max_length=255, 
        db_index=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ]
    )
    email = models.EmailField(
        validators=[EmailValidator()],
        blank=True,
        null=True
    )
    address = models.TextField()
    location = models.CharField(max_length=255, db_index=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['contact']),
            models.Index(fields=['location']),
        ]

    def __str__(self):
        return self.name

class FaqCategory(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "FAQ Categories"

    def __str__(self):
        return self.name

class NtcFaq(BaseModel):
    question = models.TextField()
    answer = models.TextField()
    category = models.ForeignKey(
        FaqCategory, 
        on_delete=models.CASCADE,
        related_name='faqs'
    )

    class Meta:
        indexes = [
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.question[:50]
