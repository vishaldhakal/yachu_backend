from rest_framework import serializers
from .models import StallBooking,SponsorBooking

class StallBookingSerializer(serializers.ModelSerializer):
      class Meta:
         model = StallBooking
         fields = '__all__'

class StallBookingSmallSerializer(serializers.ModelSerializer):
      class Meta:
         model = StallBooking
         fields = ["company", "stall_no", "status"]

class SponsorBookingSerializer(serializers.ModelSerializer):
      class Meta:
         model = SponsorBooking
         fields = "__all__"