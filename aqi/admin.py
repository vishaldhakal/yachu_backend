from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import AQI


@admin.register(AQI)
class AQIAdmin(ModelAdmin):
    list_display = ["id", "aqi", "dateTime"]
    list_filter = ["dateTime"]
    search_fields = ["aqi"]
    readonly_fields = ["dateTime"]
    ordering = ["-dateTime"]
