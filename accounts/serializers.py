from rest_framework import serializers

from .models import CustomUser, Profile, Organization
from django.db.models import Sum


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = ['id', 'name', 'person_in_charge', 'phone_number', 'address',
                  'remarks', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class OrganizationDetailSerializer(serializers.ModelSerializer):
    total_receivable = serializers.SerializerMethodField()
    total_payable = serializers.SerializerMethodField()
    total_received = serializers.SerializerMethodField()
    total_paid = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()

    def get_balance(self, obj):
        from finance_management.serializers import FinanceRecordBalanceSerializer
        return FinanceRecordBalanceSerializer(obj.financerecord_set.all(), many=True).data

    def get_total_receivable(self, obj):
        return obj.financerecord_set.filter(transaction_type='Receivable').aggregate(Sum('amount'))['amount__sum'] or 0

    def get_total_payable(self, obj):
        return obj.financerecord_set.filter(transaction_type='Payable').aggregate(Sum('amount'))['amount__sum'] or 0

    def get_total_received(self, obj):
        return obj.financerecord_set.filter(transaction_type='Received').aggregate(Sum('amount'))['amount__sum'] or 0

    def get_total_paid(self, obj):
        return obj.financerecord_set.filter(transaction_type='Paid').aggregate(Sum('amount'))['amount__sum'] or 0

    class Meta:
        model = Organization
        fields = ['id', 'name', 'person_in_charge', 'phone_number', 'address',
                  'remarks',
                  'total_receivable', 'total_payable', 'total_received', 'total_paid', 'balance']
        read_only_fields = ['created_at', 'updated_at']


class OrganizationSmallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = ['id', 'name', 'person_in_charge', 'phone_number', 'address']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password',
                  'phone_number', 'address']
        extra_kwargs = {'password': {'write_only': True}}


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'balance']
