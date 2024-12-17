from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import qrcode
from io import BytesIO
from django.core.files import File
import json
from django.core.files.base import ContentFile

class Topic(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    venue = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("End date cannot be before start date")

    def __str__(self):
        return self.name

class TimeSlot(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='time_slots')
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(default=timezone.now)
    max_participants = models.IntegerField(default=0)
    current_participants = models.IntegerField(default=0)

    def is_available(self):
        return self.current_participants < self.max_participants
    
    def available_spots(self):
        return self.max_participants - self.current_participants

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time")
        if self.max_participants < 1:
            raise ValidationError("Maximum participants must be at least 1")

    def __str__(self):
        return f"{self.topic.name}: {self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')}"

class Registration(models.Model):
    REGISTRATION_TYPES = [
        ('SINGLE', 'Single Person'),
        ('GROUP', 'Group'),
        ('EXPO_ACCESS', 'Expo Access')
    ]
    PAYMENT_METHODS = [
        ('Nabil_Bank', 'Nabil Bank'),
    ]
    REGISTRATION_STATUS = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled')
    ]

    PRICE_CONFIG = {
        'SINGLE': 300,
        'GROUP': 1500,
        'EXPO_ACCESS': 2100
    }

    # Basic Fields
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    registration_type = models.CharField(max_length=20, choices=REGISTRATION_TYPES)
    status = models.CharField(max_length=20, choices=REGISTRATION_STATUS, default='PENDING')
    
    # Participant Info
    full_name = models.CharField(max_length=200)
    qualification = models.CharField(max_length=20, choices=[
        ('Under SEE', 'Under SEE'),
        ('10+2', '10+2'),
        ('Graduate', 'Graduate'),
        ('Post Graduate', 'Post Graduate'),
    ])
    gender = models.CharField(max_length=10, choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ])
    age = models.IntegerField(validators=[MinValueValidator(14)])
    address = models.TextField()
    mobile_number = models.CharField(
        max_length=20, 
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'"
        )]
    )
    email = models.EmailField()
    
    # Payment and Status
    total_participants = models.IntegerField(validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_screenshot = models.ImageField(upload_to='payments/', null=True, blank=True)
    
    # Flags
    agreed_to_no_refund = models.BooleanField(default=False)
    is_early_bird = models.BooleanField(default=False)
    is_expo_access = models.BooleanField(default=False)
    is_free_entry = models.BooleanField(default=False)
    
    # QR Code
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def generate_qr_code(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        qr_data = {
            'registration_id': self.id,
            'participant_name': self.full_name,
            'event': self.time_slot.topic.name,
            'date': self.time_slot.topic.start_date.isoformat(),
            'time': f"{self.time_slot.start_time.strftime('%H:%M')} - {self.time_slot.end_time.strftime('%H:%M')}",
            'type': self.registration_type
        }
        
        qr.add_data(json.dumps(qr_data))
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        blob = BytesIO()
        img.save(blob, 'PNG')
        
        self.qr_code.save(
            f'qr_code_{self.id}.png',
            ContentFile(blob.getvalue()),
            save=False
        )

    def send_confirmation_email(self):
        try:
            # Render email template
            html_message = render_to_string('emails/registration_confirmation.html', {
                'registration': self
            })

            # Send email
            send_mail(
                subject=f'Registration Confirmation - {self.time_slot.topic.name}',
                message=f'''
                Dear {self.full_name},
                
                Your registration for {self.time_slot.topic.name} has been confirmed.
                
                Event Details:
                Topic: {self.time_slot.topic.name}
                Venue: {self.time_slot.topic.venue}
                Date: {self.time_slot.topic.start_date}
                Time: {self.time_slot.start_time} - {self.time_slot.end_time}
                
                Please arrive 15 minutes before the session starts.
                Bring a valid ID for verification.
                
                Best regards,
                Event Team
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.email],
                html_message=html_message,
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send email: {str(e)}")

    def save(self, *args, **kwargs):
        # Check early bird eligibility
        early_bird_date = timezone.datetime(2025, 1, 18).date()
        self.is_early_bird = timezone.now().date() <= early_bird_date

        # Calculate total price
        if self.registration_type == 'SINGLE':
            self.total_price = self.PRICE_CONFIG['SINGLE'] * self.total_participants
        elif self.registration_type == 'GROUP':
            self.total_price = self.PRICE_CONFIG['GROUP']
        elif self.registration_type == 'EXPO_ACCESS':
            self.total_price = self.PRICE_CONFIG['EXPO_ACCESS']

        # For new registrations
        is_new = self._state.adding
        
        # Save the instance first to get an ID
        super().save(*args, **kwargs)
        
        # Generate QR code and send email for new registrations
        if is_new and self.status == 'CONFIRMED':
            self.generate_qr_code()
            self.send_confirmation_email()
            super().save(update_fields=['qr_code'])

    def __str__(self):
        return f"{self.full_name} - {self.time_slot.topic.name} ({self.created_at.strftime('%Y-%m-%d %H:%M:%S')})"