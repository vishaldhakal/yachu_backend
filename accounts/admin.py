from django.contrib import admin
from .models import CustomUser, Organization, Profile,Department
from unfold.admin import ModelAdmin


class UserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'phone_number',
                    'opening_balance', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('username', 'email')


class DepartmentAdmin(ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

class OrganizationAdmin(ModelAdmin):
    list_display = ('name', 'person_in_charge', 'phone_number', 'address')
    search_fields = ('name', 'person_in_charge')


class ProfileAdmin(ModelAdmin):
    list_display = ('user', 'profile_picture')
    search_fields = ('user__username', 'profile_picture')


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Department, DepartmentAdmin)
