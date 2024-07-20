from django.db import models

class StallBooking(models.Model):

    STALL_TYPE_CHOICES = [
         ('National Prime', 'National Prime'),
         ('National General', 'National General'),
         ('International', 'International'),
         ('Agro & MSME', 'Agro & MSME'),
         ('Automobiles', 'Automobiles'),
         ('Food Stalls', 'Food Stalls'),
         ('BDS Providers Stall', 'BDS Providers Stall'),
    ]

    MERGE_CHOICES = [
        ('Merge', 'Merge'),
        ('Separate', 'Separate'),
    ]

    STATUS = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    # Organization/Company Information
    company = models.CharField(max_length=255)
    address = models.TextField()
    chief_executive = models.CharField(max_length=255)
    phone = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    email = models.EmailField()
    status = models.CharField(max_length=100, choices=STATUS, default='Pending')

    # Stall Information
    stall_type = models.CharField(max_length=200, choices=STALL_TYPE_CHOICES)
    stall_no = models.CharField(max_length=200)
    merge_or_separate = models.CharField(max_length=100, choices=MERGE_CHOICES)

    # Payment Information
    voucher = models.FileField(upload_to='vouchers/')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    advance_amount = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_in_words = models.TextField()

    # Terms and Conditions
    terms_and_conditions_accepted = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company} - Stall {self.stall_no}"

    class Meta:
        verbose_name = "Stall Booking"
        verbose_name_plural = "Stall Bookings"