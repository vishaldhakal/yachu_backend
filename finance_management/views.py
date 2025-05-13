from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, DateTimeFilter, NumberFilter, CharFilter
from .models import FinanceRecord
from .serializers import FinanceRecordListSerializer, FinanceRecordSerializer

# Create your views here.


class FinanceRecordFilter(FilterSet):
    # Filter by date range
    organization = CharFilter(
        field_name='organization__id', lookup_expr='icontains')
    date_after = DateTimeFilter(field_name='created_at', lookup_expr='gte')
    date_before = DateTimeFilter(field_name='created_at', lookup_expr='lte')

    # Filter by transaction type
    transaction_type = CharFilter(
        field_name='transaction_type', lookup_expr='icontains')

    class Meta:
        model = FinanceRecord
        fields = ['organization', 'transaction_type',
                  'date_after', 'date_before']


class FinanceRecordListCreateView(generics.ListCreateAPIView):
    queryset = FinanceRecord.objects.all().order_by('-created_at')
    serializer_class = FinanceRecordSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = FinanceRecordFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FinanceRecordListSerializer
        return FinanceRecordSerializer

    def perform_create(self, serializer):
        # Automatically set the organization and user
        serializer.save()


class FinanceRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FinanceRecordSerializer
    permission_classes = [IsAuthenticated]
