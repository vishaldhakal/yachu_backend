from django.contrib import admin
from .models import StallBooking,SponsorBooking
from unfold.admin import ModelAdmin

admin.site.register(StallBooking,ModelAdmin)
admin.site.register(SponsorBooking,ModelAdmin)
