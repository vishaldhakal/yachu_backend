from rest_framework import serializers
from .models import Eventregistration

class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eventregistration
        fields = '__all__'
        
    def validate(self, data):
        """
        Check that arrival date is before departure date
        """
        if data.get('arrival_date') and data.get('departure_date'):
            if data['arrival_date'] > data['departure_date']:
                raise serializers.ValidationError({
                    "departure_date": "Departure date must be after arrival date"
                })
        return data 