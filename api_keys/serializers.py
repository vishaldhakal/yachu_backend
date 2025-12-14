from rest_framework import serializers

from .models import APIKey


class APIKeySerializer(serializers.ModelSerializer):
    """Serializer for full CRUD operations on API keys."""

    class Meta:
        model = APIKey
        fields = [
            "id",
            "name",
            "key",
            "usage_count",
            "is_active",
            "last_used_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "usage_count",
            "last_used_at",
            "created_at",
            "updated_at",
        ]


class APIKeyUsageSerializer(serializers.ModelSerializer):
    """Read-only serializer for returning rotated keys with usage stats."""

    class Meta:
        model = APIKey
        fields = ["id", "name", "key", "usage_count", "last_used_at"]
        read_only_fields = ["id", "name", "key", "usage_count", "last_used_at"]
