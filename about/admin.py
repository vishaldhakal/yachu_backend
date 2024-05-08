from django.contrib import admin
from .models import Franchise
from unfold.admin import ModelAdmin

admin.site.register(Franchise,ModelAdmin)