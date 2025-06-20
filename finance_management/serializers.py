from rest_framework import serializers
from .models import FinanceRecord, Department, Stock, Invoice, InvoiceItem
from accounts.serializers import DepartmentSerializer, DepartmentSmallSerializer, OrganizationSmallSerializer, UserSerializer, ProjectSerializer, OrganizationSerializer, UserSmallSerializer
from accounts.models import CustomUser, Project, Organization


class FinanceRecordSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), required=False, allow_null=True)
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), required=False, allow_null=True)
    organization = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(), required=False, allow_null=True)
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), required=False, allow_null=True)
    project_slug = serializers.CharField(
        write_only=True, required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = FinanceRecord
        fields = ['id', 'user', 'organization', 'project', 'transaction_type', 'department',
                  'amount', 'payment_method', 'remarks', 'due_date', 'created_at', 'updated_at', 'project_slug']
        read_only_fields = ['created_at', 'updated_at']

    def validate_project_slug(self, value):
        if value and value.strip():
            try:
                Project.objects.get(slug=value)
            except Project.DoesNotExist:
                raise serializers.ValidationError(
                    "Project with this slug does not exist")
        return value

    def create(self, validated_data):
        # Remove project_slug from validated_data
        project_slug = validated_data.pop('project_slug', None)
        if project_slug and project_slug.strip():
            try:
                project = Project.objects.get(slug=project_slug)
                validated_data['project'] = project
            except Project.DoesNotExist:
                pass

        # Create the finance record
        return super().create(validated_data)

    def update(self, instance, validated_data):
        project_slug = validated_data.pop('project_slug', None)
        if project_slug and project_slug.strip():
            try:
                project = Project.objects.get(slug=project_slug)
                instance.project = project
            except Project.DoesNotExist:
                pass
        # Update the finance record
        return super().update(instance, validated_data)


class FinanceRecordListSerializer(serializers.ModelSerializer):
    department = DepartmentSmallSerializer()
    user = UserSmallSerializer()
    organization = OrganizationSmallSerializer()
    project = ProjectSerializer()

    class Meta:
        model = FinanceRecord
        fields = ['id', 'user', 'organization', 'project', 'transaction_type', 'department',
                  'amount', 'payment_method', 'remarks', 'due_date', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class FinanceRecordBalanceSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    user = UserSerializer()
    organization = OrganizationSerializer()
    project = ProjectSerializer()

    class Meta:
        model = FinanceRecord
        fields = ['id', 'user', 'organization', 'project', 'transaction_type', 'department',
                  'amount', 'payment_method', 'remarks', 'due_date', 'created_at', 'updated_at']


class StockSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), required=False, allow_null=True)
    product_code = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Stock
        fields = '__all__'


class StockListSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()

    class Meta:
        model = Stock
        fields = ['id', 'product_name', 'product_code', 'quantity',
                  'price', 'remarks', 'department', 'created_at', 'updated_at']


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
            'discount', 'discount_type', 'vat', 'total_amount', 'additional_notes', 'payment_terms',
            'bank_name', 'account_name', 'account_number', 'signature',
            'items', 'status'
        ]

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("At least one item is required")
        return items

    def create(self, validated_data):
        items_data = validated_data.pop('items')

        # Create the invoice
        invoice = Invoice.objects.create(**validated_data)

        # Create invoice items
        for item_data in items_data:
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
                InvoiceItem.objects.create(invoice=instance, **item_data)

        return instance


class InvoiceSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'invoice_number', 'bill_to_name',
                  'invoice_date', 'due_date', 'total_amount', 'status']
