from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from .filters import AQIFilter
from .models import AQI
from .selectors.aqi_selector import get_all_aqi, get_latest_aqi
from .serializers import AQISerializer


class AQIPagination(PageNumberPagination):
    """
    Pagination class for AQI list endpoints.
    """

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class AQIListCreateAPIView(generics.ListCreateAPIView):
    """
    API view for listing all AQI records and creating new AQI readings.
    GET: Returns a list of all AQI records (paginated, filterable, orderable)
    POST: Creates a new AQI record
    """

    queryset = AQI.objects.all()
    serializer_class = AQISerializer
    permission_classes = [AllowAny]
    pagination_class = AQIPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = AQIFilter
    ordering_fields = ["dateTime", "aqi"]
    ordering = ["-dateTime"]

    def get_queryset(self):
        return get_all_aqi()


class LatestAQIAPIView(generics.RetrieveAPIView):
    """
    API view for retrieving the single latest AQI reading.
    GET: Returns the most recent AQI record
    """

    serializer_class = AQISerializer
    permission_classes = [AllowAny]

    def get_object(self) -> AQI:
        latest_aqi = get_latest_aqi()
        if latest_aqi is None:
            raise Http404("No AQI record found.")
        return latest_aqi


class AQIRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting a specific AQI reading by ID.
    GET: Returns a single AQI record
    PUT/PATCH: Updates an AQI record
    DELETE: Deletes an AQI record
    """

    queryset = AQI.objects.all()
    serializer_class = AQISerializer
    permission_classes = [AllowAny]
