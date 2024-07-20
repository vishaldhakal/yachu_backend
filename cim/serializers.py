from rest_framework import serializers
from .models import StallBooking

class StallBookingSerializer(serializers.ModelSerializer):
      class Meta:
         model = StallBooking
         fields = '__all__'