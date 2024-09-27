from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer
from .models import Order, Product
from rest_framework.permissions import IsAuthenticated
from accounts.models import CustomUser

# Create your views here.

class OrderListCreateView(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(convinced_by=1)

    def post(self, request, *args, **kwargs):
        data = request.data
        user = CustomUser.objects.get(id=1)
        convinced_by = user
        
        # Extract order data
        order_data = {
            'convinced_by': convinced_by,
            'full_name': data.get('full_name'),
            'email': data.get('email'),
            'delivery_location': data.get('delivery_location'),
            'landmark': data.get('landmark'),
            'phone_number': data.get('phone_number'),
            'alternate_phone_number': data.get('alternate_phone_number'),
            'delivery_charge': data.get('delivery_charge'),
            'payment_method': data.get('payment_method'),
            'payment_screenshot': data.get('payment_screenshot'),
            'order_status': data.get('order_status', 'Pending'),
            'shampoo': data.get('shampoo')
        }

        # Create order
        order = Order.objects.create(**order_data)

        # Extract and create products
        products_data = data.get('products', [])
        for product_data in products_data:
            Product.objects.create(
                order=order,
                name=product_data.get('name'),
                price=product_data.get('price')
            )

        # Recalculate total amount
        order.calculate_total_amount()
        order.save()

        # Fetch the updated order with products
        updated_order = Order.objects.prefetch_related('products').get(id=order.id)
        serializer = OrderSerializer(updated_order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(convinced_by=1)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data
        
        # Update order data
        order_fields = [
            'full_name', 'email', 'delivery_location', 'landmark', 'phone_number',
            'alternate_phone_number', 'delivery_charge', 'payment_method',
            'payment_screenshot', 'order_status', 'shampoo'
        ]
        for field in order_fields:
            if field in data:
                setattr(instance, field, data[field])

        # Handle product data
        products_data = data.get('products', [])
        if products_data:
            # Clear existing products
            instance.products.all().delete()
            # Create new products
            for product_data in products_data:
                Product.objects.create(
                    order=instance,
                    name=product_data.get('name'),
                    price=product_data.get('price')
                )

        instance.save()
        instance.calculate_total_amount()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        order = self.get_object()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        order = self.get_object()
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)







