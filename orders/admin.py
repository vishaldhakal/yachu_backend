from django.contrib import admin
from unfold.admin import ModelAdmin,StackedInline
from .models import Order,Product

class ProductInline(StackedInline):
    model = Product
    extra = 1

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    inlines = [ProductInline]
    list_display = ('full_name', 'email', 'phone_number', 'total_amount', 'order_status', 'created_at')
    list_filter = ('order_status', 'payment_method')
    search_fields = ('full_name', 'email', 'phone_number')
    readonly_fields = ('total_amount',)
    