from rest_framework import serializers
from .models import StallBooking,SponsorBooking,ThematicSession,ThematicRegistration,GuidedTour,Invitation

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

class ThematicSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThematicSession
        fields = '__all__'

class ThematicRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ThematicRegistration
        fields = '__all__'

class GuidedTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuidedTour
        fields = '__all__'

class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = '__all__'