from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer, CommissionSerializer, SellerSerializer, ProductSerializer, TrackingSerializer
from .models import Order, Product, Seller, Commission,Tracking
from rest_framework.permissions import IsAuthenticated,AllowAny
from accounts.models import CustomUser

# Create your views here.

class OrderListCreateView(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Handle both form-data and raw JSON formats
            order_products = []

            # Check if order_products is already a list (JSON payload)
            if isinstance(request.data.get('order_products'), list):
                order_products = request.data.get('order_products')
            # Check if it's form-data format
            elif hasattr(request.data, 'getlist'):
                # Get the order_products string and convert it to list
                order_products_str = request.data.get('order_products')
                if order_products_str:
                    try:
                        import json
                        order_products = json.loads(order_products_str)
                    except json.JSONDecodeError:
                        return Response(
                            {"error": "Invalid order_products format"},
                            status=status.HTTP_400_BAD_REQUEST
                        )

            # Validate order products
            if not order_products:
                return Response(
                    {"error": "At least one product is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create the modified data dictionary
            modified_data = {
                'full_name': request.data.get('full_name'),
                'email': request.data.get('email'),
                'phone_number': request.data.get('phone_number'),
                'delivery_address': request.data.get('delivery_address'),
                'total_amount': request.data.get('total_amount'),
                'alternate_phone_number': request.data.get('alternate_phone_number'),
                'remarks': request.data.get('remarks'),
                'order_products': order_products
            }
            # Update the request data
            request._full_data = modified_data

            return super().create(request, *args, **kwargs)

        except Exception as e:
            return Response(
                {"error": f"Failed to create order: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

class OrderRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        order = serializer.save()
        commission = Commission.objects.get(order=order)
        commission.amount = order.total_amount * (order.seller.commission_rate / 100)
        commission.save()

class CommissionListView(ListAPIView):
    queryset = Commission.objects.all()
    serializer_class = CommissionSerializer
    permission_classes = [IsAuthenticated]

class CommissionRetrieveUpdateView(RetrieveUpdateAPIView):
    queryset = Commission.objects.all()
    serializer_class = CommissionSerializer
    permission_classes = [IsAuthenticated]

class SellerListCreateView(ListCreateAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [IsAuthenticated]

class SellerRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [IsAuthenticated]

class ProductListCreateView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


class TrackingListCreateView(ListCreateAPIView):
    queryset = Tracking.objects.all()
    serializer_class = TrackingSerializer
    permission_classes = [AllowAny]

class TrackingRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Tracking.objects.all()
    serializer_class = TrackingSerializer
    permission_classes = [AllowAny]