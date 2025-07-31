from django.contrib import admin
from .models import Contact
from unfold.admin import ModelAdmin
# Register your models here.


admin.site.register(Contact, ModelAdmin)
