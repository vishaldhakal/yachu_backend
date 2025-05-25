from rest_framework import serializers
from .models import FinanceRecord
from accounts.serializers import OrganizationSmallSerializer
from accounts.models import Organization


class FinanceRecordSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(), required=False)

    class Meta:
        model = FinanceRecord
        fields = ['id', 'organization', 'transaction_type',
                  'amount', 'remarks', 'due_date', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):

        # Create the finance record
        return super().create(validated_data)


class FinanceRecordListSerializer(serializers.ModelSerializer):
    organization = OrganizationSmallSerializer()

    class Meta:
        model = FinanceRecord
        fields = ['id', 'organization', 'transaction_type',
                  'amount', 'remarks', 'due_date', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class FinanceRecordBalanceSerializer(serializers.ModelSerializer):
    organization = OrganizationSmallSerializer()

    class Meta:
        model = FinanceRecord
        fields = ['id', 'organization', 'transaction_type', 'amount',
                  'remarks', 'due_date', 'created_at']
