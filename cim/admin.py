from django.contrib import admin
from .models import StallBooking,SponsorBooking,ThematicSession, ThematicRegistration, GuidedTour
from unfold.admin import ModelAdmin
from django.db import models
# Register your models here.

from tinymce.widgets import TinyMCE

class TinyMce(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }


admin.site.register(StallBooking,ModelAdmin)
admin.site.register(SponsorBooking,ModelAdmin)
admin.site.register(ThematicSession,TinyMce)
admin.site.register(ThematicRegistration,ModelAdmin)
admin.site.register(GuidedTour,ModelAdmin)
