from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

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

    def create(self, request, *args, **kwargs):
        print("=== AQI POST Request Payload ===")
        print(request.data)

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("=== AQI POST Validation Error ===")
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            incoming_aqi = serializer.validated_data.get("aqi")
            incoming_date_time = serializer.validated_data.get("dateTime")
            latest_aqi = get_latest_aqi()

            is_unchanged = False
            if latest_aqi:
                current_val = str(latest_aqi.aqi).strip()
                new_val = str(incoming_aqi).strip()
                if current_val == new_val:
                    is_unchanged = True
                else:
                    try:
                        is_unchanged = float(current_val) == float(new_val)
                    except (ValueError, TypeError):
                        is_unchanged = False

            if is_unchanged:
                print(
                    f"=== AQI POST: AQI unchanged ({latest_aqi.aqi}). Updating dateTime to {incoming_date_time} ==="
                )
                latest_aqi.dateTime = incoming_date_time
                latest_aqi.save(update_fields=["dateTime"])
                response_serializer = self.get_serializer(latest_aqi)
                return Response(response_serializer.data, status=status.HTTP_200_OK)

            self.perform_create(serializer)
        except Exception as exc:
            print("=== AQI POST Exception ===")
            print(exc)
            raise exc

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


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
