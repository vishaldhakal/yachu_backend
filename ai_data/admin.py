from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import AIData

# Register your models here.

admin.site.register(AIData, ModelAdmin)
