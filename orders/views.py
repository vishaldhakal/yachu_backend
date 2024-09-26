from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer
from .models import Order
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class OrderListCreateView(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(convinced_by=user)

    def post(self, request, *args, **kwargs):
        data = request.data
        convinced_by = request.user
        full_name = data.get('full_name')
        email = data.get('email')
        delivery_location = data.get('delivery_location')
        phone_number = data.get('phone_number')
        remarks = data.get('remarks')
        oil_type = data.get('oil_type')
        quantity = data.get('quantity')
        total_amount = data.get('total_amount')
        payment_method = data.get('payment_method')
        payment_screenshot = data.get('payment_screenshot')
        order_status = data.get('order_status')
        shampoo = data.get('shampoo')

        order = Order.objects.create(
            convinced_by=convinced_by,
            full_name=full_name,
            email=email,
            delivery_location=delivery_location,
            phone_number=phone_number,
            remarks=remarks,
            oil_type=oil_type,
            quantity=quantity,
            total_amount=total_amount,
            payment_method=payment_method,
            payment_screenshot=payment_screenshot,
            order_status=order_status,
            shampoo=shampoo
        )
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

#create a view to retreve,update and delete a single order
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







