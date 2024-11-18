from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Eventregistration

@admin.register(Eventregistration)
class EventRegistrationAdmin(ModelAdmin):
    list_display = ('name', 'email', 'phone', 'register_as_a', 'arrival_date', 'departure_date', 'accomodation_required')
    list_filter = ('register_as_a', 'accomodation_required', 'arrival_date', 'departure_date')
    search_fields = ('name', 'email', 'phone', 'company')
    readonly_fields = ('id',)
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Professional Details', {
            'fields': ('company', 'position', 'register_as_a', 'area_of_interest')
        }),
        ('Location & Travel', {
            'fields': ('country', 'arrival_date', 'departure_date')
        }),
        ('Accommodation', {
            'fields': ('accomodation_required', 'hotel_name')
        }),
    )
