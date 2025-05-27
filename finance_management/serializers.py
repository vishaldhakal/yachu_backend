from rest_framework import serializers
from .models import FinanceRecord, Department, Stock
from accounts.serializers import OrganizationSmallSerializer, DepartmentSerializer
from accounts.models import Organization


class FinanceRecordSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(), required=False)
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), required=False)

    class Meta:
        model = FinanceRecord
        fields = ['id', 'organization', 'transaction_type', 'department',
                  'amount', 'payment_method', 'remarks', 'due_date', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):

        # Create the finance record
        return super().create(validated_data)


class FinanceRecordListSerializer(serializers.ModelSerializer):
    organization = OrganizationSmallSerializer()
    department = DepartmentSerializer()

    class Meta:
        model = FinanceRecord
        fields = ['id', 'organization', 'transaction_type', 'department',
                  'amount', 'payment_method', 'remarks', 'due_date', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class FinanceRecordBalanceSerializer(serializers.ModelSerializer):
    organization = OrganizationSmallSerializer()
    department = DepartmentSerializer()

    class Meta:
        model = FinanceRecord
        fields = ['id', 'organization', 'transaction_type', 'department',
                  'amount', 'payment_method', 'remarks', 'due_date', 'created_at']


class StockSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Stock
        fields = '__all__'
