from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import AiData

# Register your models here.

admin.site.register(AiData, ModelAdmin)
