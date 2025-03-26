from rest_framework import serializers
from .models import Seller, OrderProduct, Order, Commission
from home.models import Product
from home.serializers import ProductSerializer, ProductSmallSerializer

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['id', 'user', 'phone_number', 'address', 'commission_rate']


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSmallSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True, source='product')

    class Meta:
        model = OrderProduct
        fields = ['id', 'product', 'product_id', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id','full_name', 'email', 'phone_number', 'alternate_phone_number', 'delivery_address',
                  'delivery_charge', 'payment_method', 'payment_screenshot', 'order_status', 'created_at',
                  'updated_at', 'total_amount', 'order_products' ]

    def create(self, validated_data):
        # Extract order products data
        order_products_data = validated_data.pop('order_products', [])
        
        # Create order
        order = Order.objects.create(**validated_data)
        
        # Create order products
        for order_product_data in order_products_data:
            product = order_product_data['product']
            quantity = order_product_data['quantity']
            OrderProduct.objects.create(order=order, product=product, quantity=quantity)
        
        return order

    def update(self, instance, validated_data):
        order_products_data = validated_data.pop('order_products', None)
        instance = super().update(instance, validated_data)

        if order_products_data is not None:
            instance.order_products.all().delete()
            for order_product_data in order_products_data:
                OrderProduct.objects.create(order=instance, **order_product_data)

        return instance

class CommissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commission
        fields = ['id', 'seller', 'order', 'amount', 'paid', 'created_at']
