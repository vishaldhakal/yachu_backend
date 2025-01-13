from rest_framework import serializers
from .models import StallBooking,SponsorBooking,ThematicSession,ThematicRegistration,GuidedTour,Invitation,SubSession,Panelist

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

class PanelistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Panelist
        fields = ['role', 'name', 'profile_image', 'company', 'location', 'biodata']


class SubSessionSerializer(serializers.ModelSerializer):
    panelists = PanelistSerializer(many=True, read_only=True)

    class Meta:
        model = SubSession
        fields = ['id', 'title', 'description', 'panelists']


class ThematicSessionSerializer(serializers.ModelSerializer):
    sub_sessions = SubSessionSerializer(many=True, read_only=True)

    class Meta:
        model = ThematicSession
        fields = ['id', 'title', 'date', 'start_time', 'end_time', 'description', 'sub_sessions']

class ThematicRegistrationSerializer(serializers.ModelSerializer):
    session=ThematicSessionSerializer(many=True,read_only=True)

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