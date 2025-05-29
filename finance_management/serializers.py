from rest_framework import serializers
from .models import FinanceRecord, Department, Stock, Tag, Invoice, InvoiceItem
from accounts.serializers import OrganizationSmallSerializer, DepartmentSerializer
from accounts.models import Organization


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class FinanceRecordSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(), required=False)
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), required=False)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, required=False)

    class Meta:
        model = FinanceRecord
        fields = ['id', 'organization', 'transaction_type', 'department',
                  'amount', 'payment_method', 'remarks', 'due_date', 'tags', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):

        # Create the finance record
        return super().create(validated_data)


class FinanceRecordListSerializer(serializers.ModelSerializer):
    organization = OrganizationSmallSerializer()
    department = DepartmentSerializer()
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = FinanceRecord
        fields = ['id', 'organization', 'transaction_type', 'department',
                  'amount', 'payment_method', 'remarks', 'due_date', 'tags', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class FinanceRecordBalanceSerializer(serializers.ModelSerializer):
    organization = OrganizationSmallSerializer()
    department = DepartmentSerializer()
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = FinanceRecord
        fields = ['id', 'organization', 'transaction_type', 'department',
                  'amount', 'payment_method', 'remarks', 'due_date', 'tags', 'created_at', 'updated_at']


class StockSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Stock
        fields = '__all__'


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ['name', 'description', 'quantity', 'rate', 'amount']


class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = [
            'id',
            'bill_from_name', 'bill_from_address', 'bill_from_email', 'bill_from_phone',
            'bill_to_name', 'bill_to_address', 'bill_to_email', 'bill_to_phone',
            'invoice_number', 'invoice_date', 'due_date', 'currency', 'logo',
            'discount', 'tax', 'total_amount', 'additional_notes', 'payment_terms',
            'bank_name', 'account_name', 'account_number', 'signature',
            'items', 'status'
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        invoice = Invoice.objects.create(**validated_data)

        for item_data in items_data:
            # Calculate amount if not provided
            if 'amount' not in item_data:
                item_data['amount'] = item_data['quantity'] * item_data['rate']
            InvoiceItem.objects.create(invoice=invoice, **item_data)

        return invoice

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)

        # Update invoice fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update items if provided
        if items_data is not None:
            # Delete existing items
            instance.items.all().delete()

            # Create new items
            for item_data in items_data:
                # Calculate amount if not provided
                if 'amount' not in item_data:
                    item_data['amount'] = item_data['quantity'] * \
                        item_data['rate']
                InvoiceItem.objects.create(invoice=instance, **item_data)

        return instance


class InvoiceSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'invoice_number', 'bill_to_name',
                  'invoice_date', 'due_date', 'total_amount', 'status']
