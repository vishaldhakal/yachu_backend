from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe
from tinymce.widgets import TinyMCE
from unfold.admin import ModelAdmin, TabularInline

from .models import (
    BillOfMaterial,
    Blog,
    BlogCategory,
    BlogTag,
    Component,
    ComponentModel,
    ComponentPurchase,
    ComponentPurchaseItem,
    Contact,
    Faq,
    Gallery,
    Image,
    Inventory,
    LeaveForm,
    OurPartner,
    Project,
    ProjectDailyUpdate,
    ProjectDemo,
    ProjectInventoryUsed,
    ProjectTool,
    Service,
    TeamMember,
    TechnicalDocument,
    Testimonial,
    Vendor,
)

# Register your models here.


class TinyMCEAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }


class ImageInline(TabularInline):
    model = Image
    extra = 1
    tab = True


class ProjectDemoInline(TabularInline):
    model = ProjectDemo
    extra = 1
    tab = True


class TechnicalDocumentInline(TabularInline):
    model = TechnicalDocument
    extra = 1
    tab = True


class ProjectInventoryUsedInline(TabularInline):
    model = ProjectInventoryUsed
    extra = 1
    tab = True


class ProjectDailyUpdateInline(TabularInline):
    model = ProjectDailyUpdate
    extra = 1
    tab = True


class ComponentModelInline(TabularInline):
    model = ComponentModel
    extra = 1
    prepopulated_fields = {"slug": ("name",)}
    tab = True


class ComponentPurchaseItemInline(TabularInline):
    model = ComponentPurchaseItem
    extra = 1
    tab = True


class InventoryInline(TabularInline):
    model = Inventory
    extra = 1
    tab = True


class BillOfMaterialInline(TabularInline):
    model = BillOfMaterial
    extra = 1
    tab = True


class ComponentInline(TabularInline):
    model = Component
    extra = 1
    prepopulated_fields = {"slug": ("name",)}
    tab = True


@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ["title", "slug", "description", "created_at", "updated_at"]
    prepopulated_fields = {"slug": ("title",)}

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if form.base_fields.get("description"):
            form.base_fields["description"].widget = TinyMCE()
        return form


@admin.register(Project)
class ProjectAdmin(TinyMCEAdmin):
    list_display = [
        "title",
        "slug",
        "get_categories",
        "status",
        "created_at",
        "updated_at",
    ]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [
        ImageInline,
        ProjectDemoInline,
        TechnicalDocumentInline,
        ProjectInventoryUsedInline,
        ProjectDailyUpdateInline,
    ]

    def get_categories(self, obj):
        return mark_safe(
            "<br>".join([category.title for category in obj.category.all()])
        )

    get_categories.short_description = "Categories"


@admin.register(Vendor)
class VendorAdmin(ModelAdmin):
    list_display = ["name", "slug", "phone_no", "created_at", "updated_at"]
    search_fields = ["name", "phone_no"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [BillOfMaterialInline, ComponentInline]


@admin.register(BillOfMaterial)
class BillOfMaterialAdmin(ModelAdmin):
    list_display = ["file", "vendor", "created_at", "updated_at"]
    list_filter = ["vendor"]


@admin.register(ProjectTool)
class ProjectToolAdmin(ModelAdmin):
    list_display = ["name", "slug", "created_at", "updated_at"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Component)
class ComponentAdmin(ModelAdmin):
    list_display = ["name", "slug", "vendor", "created_at", "updated_at"]
    list_filter = ["vendor"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ComponentModelInline]


@admin.register(ComponentModel)
class ComponentModelAdmin(ModelAdmin):
    list_display = ["name", "slug", "component", "created_at", "updated_at"]
    list_filter = ["component"]
    search_fields = ["name", "specs"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [InventoryInline]


@admin.register(ComponentPurchase)
class ComponentPurchaseAdmin(ModelAdmin):
    list_display = [
        "vendor",
        "purchase_date",
        "total_price",
        "created_at",
        "updated_at",
    ]
    list_filter = ["vendor", "purchase_date"]
    search_fields = ["vendor__name", "notes"]
    inlines = [ComponentPurchaseItemInline]


@admin.register(Inventory)
class InventoryAdmin(ModelAdmin):
    list_display = ["component_model", "quantity", "created_at", "updated_at"]
    list_filter = ["component_model"]


@admin.register(ProjectInventoryUsed)
class ProjectInventoryUsedAdmin(ModelAdmin):
    list_display = ["project", "inventory", "quantity", "created_at", "updated_at"]
    list_filter = ["project"]


@admin.register(ProjectDailyUpdate)
class ProjectDailyUpdateAdmin(ModelAdmin):
    list_display = [
        "project",
        "task",
        "decision",
        "problem",
        "created_at",
        "updated_at",
    ]
    list_filter = ["project"]
    search_fields = ["project__title", "task", "decision", "problem"]


@admin.register(ProjectDemo)
class ProjectDemoAdmin(ModelAdmin):
    list_display = ["project", "video_url", "video_file", "created_at", "updated_at"]
    list_filter = ["project"]
    search_fields = ["project__title"]


@admin.register(TechnicalDocument)
class TechnicalDocumentAdmin(ModelAdmin):
    list_display = ["project", "file", "created_at", "updated_at"]
    list_filter = ["project"]
    search_fields = ["project__title"]


@admin.register(BlogCategory)
class BlogCategoryAdmin(ModelAdmin):
    list_display = ["title", "slug", "created_at", "updated_at"]


@admin.register(BlogTag)
class BlogTagAdmin(ModelAdmin):
    list_display = ["title", "created_at", "updated_at"]


@admin.register(Blog)
class BlogAdmin(TinyMCEAdmin):
    list_display = ["title", "slug", "created_at", "updated_at"]


@admin.register(Contact)
class ContactAdmin(ModelAdmin):
    list_display = [
        "name",
        "email",
        "phone",
        "message",
        "company",
        "created_at",
    ]
    list_filter = ["company"]
    search_fields = ["company", "name", "email"]


@admin.register(TeamMember)
class TeamMemberAdmin(ModelAdmin):
    list_display = ["name", "designation", "created_at", "updated_at"]


@admin.register(Faq)
class FaqAdmin(ModelAdmin):
    list_display = ["question", "created_at", "updated_at"]


@admin.register(Testimonial)
class TestimonialAdmin(ModelAdmin):
    list_display = ["name", "rating", "designation", "created_at", "updated_at"]


@admin.register(OurPartner)
class OurPartnerAdmin(ModelAdmin):
    list_display = ["title", "website_url", "created_at", "updated_at"]


@admin.register(Gallery)
class GalleryAdmin(ModelAdmin):
    list_display = ["title", "media_type", "created_at", "updated_at"]


@admin.register(LeaveForm)
class LeaveFormAdmin(ModelAdmin):
    list_display = [
        "employee_name",
        "reason_of_leave",
        "days",
        "leave_from_date",
        "leave_to_date",
        "approved_by",
        "created_at",
    ]
    list_filter = ["reason_of_leave", "approved_by"]
    search_fields = ["employee_name", "employee_email", "brief_reason"]
