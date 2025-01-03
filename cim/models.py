from django.db import models

class StallBooking(models.Model):

    STALL_TYPE_CHOICES = [
         ('National Prime', 'National Prime'),
         ('National General', 'National General'),
         ('International', 'International'),
         ('Agro and MSME', 'Agro and MSME'),
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
    
    def has_paid_all(self):
        return self.remaining_amount == 0

    class Meta:
        verbose_name = "Stall Booking"
        verbose_name_plural = "Stall Bookings"


class SponsorBooking(models.Model):
    STALL_TYPE_CHOICES = [
        ('Main Sponsor', 'Main Sponsor'),
        ('Powered By Sponsor', 'Powered By Sponsor'),
        ('Platinum', 'Platinum'),
        ('Diamond', 'Diamond'),
        ('Gold', 'Gold'),
        ('Partner Sponsor', 'Partner Sponsor'),
        ('Silver', 'Silver'),
    ]

    stall_type = models.CharField(max_length=200, choices=STALL_TYPE_CHOICES)
    stall_id = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200,blank=True, null=True)
    company_email = models.CharField(max_length=200,blank=True, null=True)
    contact_number = models.CharField(max_length=200,blank=True, null=True)

    def __str__(self):
        return f"{self.company_name} - {self.stall_id}"

# Model for Thematic Session
class ThematicSession(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    start_time = models.TimeField()
    end_time=models.TimeField(blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.title


# Model for Thematic Registration
class ThematicRegistration(models.Model):
    PARTICIPANT_TYPE_CHOICES = [
        ('Speaker', 'Speaker'),
        ('Participant', 'Participant'),
    ]
    FOOD_CHOICES = [
        ('Veg', 'Veg'),
        ('Non Veg', 'Non Veg'),
    ]
    HOTEL_ACCOMODATION_CHOICES = [
        ('Self', 'Self'),
        ('CIM', 'CIM'),
    ]
    name = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    contact = models.CharField(max_length=15)
    travel_arrive_date = models.DateField(null=True, blank=True)
    travel_back_date = models.DateField(null=True, blank=True)
    food= models.CharField(max_length=20, choices=FOOD_CHOICES,null=True, blank=True)
    hotel_accomodation= models.CharField(max_length=20, choices=HOTEL_ACCOMODATION_CHOICES,null=True, blank=True)
    participant= models.CharField(max_length=20, choices=PARTICIPANT_TYPE_CHOICES)
    sessions = models.ManyToManyField(ThematicSession, related_name='registrations')

    def __str__(self):
        return f"{self.name} - {self.organization}"
    

class GuidedTour(models.Model):
    # College Details
    college_name = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    municipality = models.CharField(max_length=255)
    ward = models.CharField(max_length=50)
   
    # Contact Details
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    contact_person_name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    mobile_no = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )    
    # Tour Details
    tour_date = models.DateField()
    number_of_students = models.PositiveIntegerField()
    STUDENT_LEVEL_CHOICES = [
        ('10+2', '10+2'),
        ('Bachelors', 'Bachelors'),
        ('Masters', 'Masters'),
        ('Mixed', 'Mixed'),
    ]
    student_level = models.CharField(
        max_length=20,
        choices=STUDENT_LEVEL_CHOICES,
        default='10+2'
    )

    def __str__(self):
        return f"{self.college_name} - {self.tour_date}"

