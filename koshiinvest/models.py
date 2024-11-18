from django.db import models

class Eventregistration(models.Model):
    REGISTER_AS_A_CHOICES = [
        ('Investor', 'Investor'),
        ('Stakeholder', 'Stakeholder'),
        ('Learner', 'Learner'),
        ('Visitor', 'Visitor'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    company = models.CharField(max_length=100,blank=True)
    position = models.CharField(max_length=100,blank=True)
    register_as_a = models.CharField(max_length=100,choices=REGISTER_AS_A_CHOICES,default='Visitor')
    area_of_interest = models.CharField(max_length=100,blank=True)
    country = models.CharField(max_length=100,blank=True)
    arrival_date = models.DateField(blank=True)
    departure_date = models.DateField(blank=True)
    accomodation_required = models.BooleanField(default=False)
    hotel_name = models.CharField(max_length=100,blank=True)


    def __str__(self):
        return self.name
