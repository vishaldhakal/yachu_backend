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
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        order = self.get_object()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        order = self.get_object()
        data = request.data
        
        order.full_name = data.get('full_name', order.full_name)
        order.email = data.get('email', order.email)
        order.delivery_location = data.get('delivery_location', order.delivery_location)
        order.phone_number = data.get('phone_number', order.phone_number)
        order.remarks = data.get('remarks', order.remarks)
        order.oil_type = data.get('oil_type', order.oil_type)
        order.quantity = data.get('quantity', order.quantity)
        order.total_amount = data.get('total_amount', order.total_amount)
        order.payment_method = data.get('payment_method', order.payment_method)
        order.payment_screenshot = data.get('payment_screenshot', order.payment_screenshot)
        order.order_status = data.get('order_status', order.order_status)
        order.shampoo = data.get('shampoo', order.shampoo)

        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        order = self.get_object()
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)







