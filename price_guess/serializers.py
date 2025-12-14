import re

from rest_framework import serializers

from .models import PriceGuess


class PriceGuessSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceGuess
        fields = [
            "id",
            "name",
            "phone_number",
            "yachu_facewash_price",
            "yachu_bodylotion_price",
            "yachu_brightening_cream_price",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def normalize_phone(self, value):
        # Remove +, spaces, hyphens
        phone = re.sub(r"[^\d]", "", value)

        # Keep last 10 digits (Nepal mobile)
        if len(phone) >= 10:
            phone = phone[-10:]

        return phone

    def validate_phone_number(self, value):
        normalized_phone = self.normalize_phone(value)

        if PriceGuess.objects.filter(phone_number=normalized_phone).exists():
            raise serializers.ValidationError(
                "You have already submitted a guess with this phone number."
            )

        return normalized_phone
