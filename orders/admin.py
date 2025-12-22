from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import Commission, InstantOrder, Order, OrderProduct, Seller, Tracking


@admin.register(Seller)
class SellerAdmin(ModelAdmin):
    list_display = ("user", "phone_number", "commission_rate")
    search_fields = ("user__username", "user__email", "phone_number")


class OrderProductInline(TabularInline):
    model = OrderProduct
    extra = 1


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    inlines = [OrderProductInline]
    list_display = (
        "full_name",
        "phone_number",
        "total_amount",
        "order_status",
        "created_at",
    )
    list_filter = ("order_status",)
    search_fields = ("full_name", "phone_number")

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None
        super().save_model(request, obj, form, change)
        if is_new:
            obj.save()  # Save again to ensure related objects can be created


@admin.register(Commission)
class CommissionAdmin(ModelAdmin):
    list_display = ("seller", "order", "amount", "paid", "created_at")
    list_filter = ("paid", "seller")
    search_fields = ("seller__user__username", "order__full_name")


@admin.register(Tracking)
class TrackingAdmin(ModelAdmin):
    list_display = ("details", "created_at", "updated_at")
    search_fields = ("details",)
    list_filter = ("created_at", "updated_at")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 10
    list_max_show_all = 100


@admin.register(InstantOrder)
class InstantOrderAdmin(ModelAdmin):
    list_display = (
        "name",
        "phone_number",
        "address",
        "quantity",
        "created_at",
    )
    list_filter = ("quantity",)
    search_fields = ("name", "phone_number")
