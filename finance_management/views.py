from datetime import datetime, timedelta
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, DateTimeFilter, CharFilter
from .models import FinanceRecord
from .serializers import FinanceRecordListSerializer, FinanceRecordSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum

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
    search_fields = ['organization__name', 'transaction_type']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FinanceRecordListSerializer
        return FinanceRecordSerializer

    def perform_create(self, serializer):
        # Automatically set the organization and user
        serializer.save()


class FinanceRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FinanceRecord.objects.all().order_by('-created_at')
    serializer_class = FinanceRecordSerializer
    permission_classes = [IsAuthenticated]


class FinanceRecordDueDateView(generics.ListAPIView):
    serializer_class = FinanceRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Calculate the date 7 days from now
        date_limit = datetime.now() + timedelta(days=7)
        return FinanceRecord.objects.filter(
            due_date__lte=date_limit,
            transaction_type__in=['Receivable', 'Payable']
        )


class FinanceRecordTotalView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        totals = {
            'total_receivable': FinanceRecord.objects.filter(transaction_type='Receivable').aggregate(Sum('amount'))['amount__sum'] or 0,
            'total_payable': FinanceRecord.objects.filter(transaction_type='Payable').aggregate(Sum('amount'))['amount__sum'] or 0,
            'total_received': FinanceRecord.objects.filter(transaction_type='Received').aggregate(Sum('amount'))['amount__sum'] or 0,
            'total_paid': FinanceRecord.objects.filter(transaction_type='Paid').aggregate(Sum('amount'))['amount__sum'] or 0,
        }
        return Response(totals, status=status.HTTP_200_OK)
