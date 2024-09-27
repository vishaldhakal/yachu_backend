from rest_framework import serializers
from .models import Order, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']

class OrderSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'convinced_by', 'full_name', 'email', 'delivery_location', 'landmark',
                  'phone_number', 'alternate_phone_number', 'delivery_charge', 'payment_method',
                  'payment_screenshot', 'order_status', 'shampoo', 'total_amount', 'products']

    def get_products(self, obj):
        products = obj.order_products.all()
        return ProductSerializer(products, many=True).data

