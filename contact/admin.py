from django.contrib import admin
from .models import Contact
from unfold.admin import ModelAdmin
# Register your models here.

class ContactAdmin(ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'message', 'created_at')
    list_filter = ('created_at')
    search_fields = ('full_name','phone')
    ordering = ('-created_at',)

admin.site.register(Contact, ContactAdmin)
