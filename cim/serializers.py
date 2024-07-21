from rest_framework import serializers
from .models import StallBooking

class StallBookingSerializer(serializers.ModelSerializer):
      class Meta:
         model = StallBooking
         fields = '__all__'

class StallBookingSmallSerializer(serializers.ModelSerializer):
      class Meta:
         model = StallBooking
         fields = ["company", "stall_no", "status"]