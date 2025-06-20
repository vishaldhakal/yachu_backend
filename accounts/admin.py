from django.contrib import admin
from .models import CustomUser, Organization, Profile, Department, OrganizationContacts, Project, ProjectNotes, ProjectReminder
from unfold.admin import ModelAdmin, TabularInline
from tinymce.widgets import TinyMCE
from django.db import models


class UserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'phone_number',
                    'opening_balance', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('username', 'email')


class DepartmentAdmin(ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


class OrganizationContactsInline(TabularInline):
    model = OrganizationContacts
    extra = 1
    tab = True


class ProjectNotesInline(TabularInline):
    model = ProjectNotes
    extra = 1
    tab = True


class ProjectReminderInline(TabularInline):
    model = ProjectReminder
    extra = 1
    tab = True


class ProjectAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'organization')
    inlines = [ProjectNotesInline, ProjectReminderInline]


class ProjectInline(TabularInline):
    model = Project
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(mce_attrs={'width': 800, 'height': 300})},
    }
    extra = 1
    tab = True


class OrganizationAdmin(ModelAdmin):
    list_display = ('name', 'person_in_charge', 'phone_number', 'address')
    search_fields = ('name', 'person_in_charge')
    inlines = [OrganizationContactsInline, ProjectInline]


class ProfileAdmin(ModelAdmin):
    list_display = ('user', 'profile_picture')
    search_fields = ('user__username', 'profile_picture')


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Project, ProjectAdmin)
