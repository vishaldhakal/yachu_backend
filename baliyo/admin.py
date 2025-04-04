from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Service, Project, Blog, Contact, TeamMember, Faq, Testimonial, Image, BlogCategory, BlogTag, OurPartner
from tinymce.widgets import TinyMCE
from django.db import models
from django.utils.safestring import mark_safe

# Register your models here.


class TinyMCEAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }


class ImageInline(TabularInline):
    model = Image
    extra = 1


@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ['title', 'slug', 'description', 'created_at', 'updated_at']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if form.base_fields.get('description'):
            form.base_fields['description'].widget = TinyMCE()
        return form


@admin.register(Project)
class ProjectAdmin(TinyMCEAdmin):
    list_display = ['title', 'slug',
                    'get_categories', 'created_at', 'updated_at']
    inlines = [ImageInline]

    def get_categories(self, obj):
        return mark_safe('<br>'.join([category.title for category in obj.category.all()]))

    get_categories.short_description = 'Categories'


@admin.register(BlogCategory)
class BlogCategoryAdmin(ModelAdmin):
    list_display = ['title', 'slug', 'created_at', 'updated_at']


@admin.register(BlogTag)
class BlogTagAdmin(ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at']


@admin.register(Blog)
class BlogAdmin(TinyMCEAdmin):
    list_display = ['title', 'slug', 'description', 'created_at', 'updated_at']


@admin.register(Contact)
class ContactAdmin(ModelAdmin):
    list_display = ['name', 'email', 'phone',
                    'message', 'created_at', 'updated_at']


@admin.register(TeamMember)
class TeamMemberAdmin(ModelAdmin):
    list_display = ['name', 'designation', 'created_at', 'updated_at']


@admin.register(Faq)
class FaqAdmin(ModelAdmin):
    list_display = ['question', 'created_at', 'updated_at']


@admin.register(Testimonial)
class TestimonialAdmin(ModelAdmin):
    list_display = ['name', 'message', 'rating',
                    'designation', 'created_at', 'updated_at']


@admin.register(OurPartner)
class OurPartnerAdmin(ModelAdmin):
    list_display = ['title', 'website_url', 'created_at', 'updated_at']
