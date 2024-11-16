from django.contrib import admin
from django.db.models import Q
from unfold.admin import ModelAdmin
from .models import (
    ServiceCategory, ServiceSubCategory, NtcService,
    NtcPackage, NtcCustomerCare, NtcFaq, FaqCategory
)

class BaseModelAdmin(ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at', 'is_active']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['name', 'description']
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(BaseModelAdmin):
    pass

@admin.register(ServiceSubCategory)
class ServiceSubCategoryAdmin(BaseModelAdmin):
    list_display = ['name', 'category', 'created_at', 'is_active']
    list_filter = ['category'] + BaseModelAdmin.list_filter

@admin.register(NtcService)
class NtcServiceAdmin(BaseModelAdmin):
    list_display = ['name', 'category', 'subcategory', 'created_at', 'is_active']
    list_filter = ['category', 'subcategory'] + BaseModelAdmin.list_filter
    prepopulated_fields = {'slug': ('name',)}

@admin.register(NtcPackage)
class NtcPackageAdmin(BaseModelAdmin):
    list_display = ['name', 'services', 'created_at', 'is_active']
    list_filter = ['services'] + BaseModelAdmin.list_filter

@admin.register(NtcCustomerCare)
class NtcCustomerCareAdmin(BaseModelAdmin):
    list_display = ['name', 'contact', 'email', 'location', 'created_at', 'is_active']
    search_fields = ['name', 'description', 'contact', 'email', 'location']

@admin.register(FaqCategory)
class FaqCategoryAdmin(BaseModelAdmin):
    pass

@admin.register(NtcFaq)
class NtcFaqAdmin(ModelAdmin):
    list_display = ['question', 'category', 'created_at', 'is_active']
    list_filter = ['category', 'is_active', 'created_at', 'updated_at']
    search_fields = ['question', 'answer']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
