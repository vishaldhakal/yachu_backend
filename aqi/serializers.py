from rest_framework import serializers

from .models import AQI


class AQISerializer(serializers.ModelSerializer):
    class Meta:
        model = AQI
        fields = ["id", "aqi", "dateTime"]
        read_only_fields = ["id"]

    def validate_aqi(self, value: str) -> str:
        """
        Validate that the AQI value is present and non-empty.
        """
        stripped_value = str(value).strip()
        if not stripped_value:
            raise serializers.ValidationError("AQI value cannot be empty.")
        return stripped_value
