from django.contrib import admin
from .models import FinanceRecord
from unfold.admin import ModelAdmin

# Register your models here.


class FinanceRecordAdmin(ModelAdmin):
    list_display = ('organization', 'transaction_type',
                    'amount', 'created_at', 'updated_at')
    search_fields = ('organization__name',)


admin.site.register(FinanceRecord, FinanceRecordAdmin)
