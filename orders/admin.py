from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Seller, OrderProduct, Order, Commission

@admin.register(Seller)
class SellerAdmin(ModelAdmin):
    list_display = ('user', 'phone_number', 'commission_rate')
    search_fields = ('user__username', 'user__email', 'phone_number')


class OrderProductInline(TabularInline):
    model = OrderProduct
    extra = 1

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    inlines = [OrderProductInline]
    list_display = ('full_name', 'phone_number', 'total_amount', 'order_status', 'created_at')
    list_filter = ('order_status',)
    search_fields = ('full_name', 'phone_number')

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None
        super().save_model(request, obj, form, change)
        if is_new:
            obj.save()  # Save again to ensure related objects can be created

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
        formset.save_m2m()
        form.instance.total_amount = sum(op.get_total_price() for op in form.instance.order_products.all()) + form.instance.delivery_charge
        form.instance.save()

@admin.register(Commission)
class CommissionAdmin(ModelAdmin):
    list_display = ('seller', 'order', 'amount', 'paid', 'created_at')
    list_filter = ('paid', 'seller')
    search_fields = ('seller__user__username', 'order__full_name')
