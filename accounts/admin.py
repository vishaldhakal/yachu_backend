from django.contrib import admin
from .models import CustomUser, Organization, Profile
from unfold.admin import ModelAdmin


class UserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('username', 'email')


class OrganizationAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class ProfileAdmin(ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user__username', 'balance')


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Profile, ProfileAdmin)
