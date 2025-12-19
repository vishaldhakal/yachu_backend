from django_filters import rest_framework as django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as rest_filters
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from home.serializers import ProductSerializer

from .models import Commission, InstantOrder, Order, Product, Seller, Tracking
from .serializers import (
    CommissionSerializer,
    InstantOrderSerializer,
    OrderSerializer,
    SellerSerializer,
    TrackingSerializer,
)

# Create your views here.


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class OrderFilter(django_filters.FilterSet):
    franchise = django_filters.CharFilter(
        field_name="franchise__slug", lookup_expr="exact"
    )
    order_status = django_filters.CharFilter(
        field_name="order_status", lookup_expr="icontains"
    )
    date_gte = django_filters.DateFilter(field_name="created_at", lookup_expr="gte")
    date_lte = django_filters.DateFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Order
        fields = ["franchise", "order_status", "date_gte", "date_lte"]


class OrderListCreateView(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        DjangoFilterBackend,
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
    ]
    filterset_class = OrderFilter
    search_fields = ["full_name", "phone_number", "email"]
    ordering = ["-created_at", "created_at"]
    pagination_class = CustomPagination

    def get_queryset(self):
        franchise_slug = self.request.query_params.get("franchise")
        if franchise_slug:
            return Order.objects.filter(franchise__slug=franchise_slug)
        return Order.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            # Handle both form-data and raw JSON formats
            order_products = []

            # Check if order_products is already a list (JSON payload)
            if isinstance(request.data.get("order_products"), list):
                order_products = request.data.get("order_products")
            # Check if it's form-data format
            elif hasattr(request.data, "getlist"):
                # Get the order_products string and convert it to list
                order_products_str = request.data.get("order_products")
                if order_products_str:
                    try:
                        import json

                        order_products = json.loads(order_products_str)
                    except json.JSONDecodeError:
                        return Response(
                            {"error": "Invalid order_products format"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

            # Validate order products
            if not order_products:
                return Response(
                    {"error": "At least one product is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Create the modified data dictionary
            modified_data = {
                "franchise": request.data.get("franchise"),
                "full_name": request.data.get("full_name"),
                "email": request.data.get("email"),
                "phone_number": request.data.get("phone_number"),
                "delivery_address": request.data.get("delivery_address"),
                "total_amount": request.data.get("total_amount"),
                "alternate_phone_number": request.data.get("alternate_phone_number"),
                "remarks": request.data.get("remarks"),
                "order_products": order_products,
            }
            # Update the request data
            request._full_data = modified_data

            return super().create(request, *args, **kwargs)

        except Exception as e:
            return Response(
                {"error": f"Failed to create order: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class OrderRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class CommissionListView(ListAPIView):
    queryset = Commission.objects.all()
    serializer_class = CommissionSerializer


class CommissionRetrieveUpdateView(RetrieveUpdateAPIView):
    queryset = Commission.objects.all()
    serializer_class = CommissionSerializer


class SellerListCreateView(ListCreateAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


class SellerRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


class ProductListCreateView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class TrackingListCreateView(ListCreateAPIView):
    queryset = Tracking.objects.all()
    serializer_class = TrackingSerializer
    permission_classes = [AllowAny]


class TrackingRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Tracking.objects.all()
    serializer_class = TrackingSerializer
    permission_classes = [AllowAny]


class InstantOrderListCreateView(ListCreateAPIView):
    queryset = InstantOrder.objects.all()
    serializer_class = InstantOrderSerializer


class InstantOrderRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = InstantOrder.objects.all()
    serializer_class = InstantOrderSerializer
