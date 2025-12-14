from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import APIKey


@admin.register(APIKey)
class APIKeyAdmin(ModelAdmin):
    """Admin interface for API Key management."""

    list_display = [
        "name",
        "key",
        "usage_count",
        "is_active",
        "last_used_at",
        "created_at",
    ]
    search_fields = ["name", "key"]
