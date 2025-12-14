from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import PriceGuess


@admin.register(PriceGuess)
class PriceGuessAdmin(ModelAdmin):
    list_display = [
        "name",
        "phone_number",
        "yachu_facewash_price",
        "yachu_bodylotion_price",
        "yachu_brightening_cream_price",
        "created_at",
    ]
    list_filter = ["created_at"]
    search_fields = ["name", "phone_number"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
