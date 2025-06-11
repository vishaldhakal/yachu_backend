from django.contrib import admin
from .models import FinanceRecord, Stock, Invoice, InvoiceItem
from unfold.admin import ModelAdmin, TabularInline

# Register your models here


class FinanceRecordAdmin(ModelAdmin):
    list_display = ('project', 'transaction_type',
                    'amount', 'created_at', 'updated_at')
    search_fields = ('project__name',)


class StockAdmin(ModelAdmin):
    list_display = ('product_name', 'product_code',
                    'price', 'quantity', 'created_at', 'updated_at')
    search_fields = ('product_name',)

class InvoiceItemAdmin(TabularInline):
    model = InvoiceItem
    tab=True

class InvoiceAdmin(ModelAdmin):
    list_display = ('invoice_number', 'invoice_date',
                    'due_date', 'currency', 'created_at', 'updated_at')
    search_fields = ('invoice_number',)
    inlines = [InvoiceItemAdmin]


admin.site.register(FinanceRecord, FinanceRecordAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Invoice, InvoiceAdmin)

