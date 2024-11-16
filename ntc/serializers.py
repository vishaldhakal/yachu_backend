from rest_framework import serializers
from .models import (
    ServiceCategory, ServiceSubCategory, NtcService, 
    NtcPackage, NtcCustomerCare, NtcFaq
)

class SearchQuerySerializer(serializers.Serializer):
    query = serializers.CharField(required=True, min_length=3)

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'description']

class ServiceSubCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = ServiceSubCategory
        fields = ['id', 'name', 'description', 'category_name']

class NtcServiceSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)

    class Meta:
        model = NtcService
        fields = ['id', 'name', 'description', 'category_name', 'subcategory_name', 'slug']

class NtcPackageSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='services.name', read_only=True)

    class Meta:
        model = NtcPackage
        fields = ['id', 'name', 'description', 'service_name']

class NtcCustomerCareSerializer(serializers.ModelSerializer):
    class Meta:
        model = NtcCustomerCare
        fields = ['id', 'name', 'description', 'contact', 'email', 'address', 'location']

class NtcFaqSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = NtcFaq
        fields = ['id', 'question', 'answer', 'category_name'] 