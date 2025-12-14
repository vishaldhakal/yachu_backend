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
