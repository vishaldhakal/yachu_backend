from datetime import datetime, timedelta
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, DateTimeFilter, CharFilter
from .models import FinanceRecord
from .serializers import FinanceRecordListSerializer, FinanceRecordSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth, TruncYear

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


class TransactionSummaryFilter(FilterSet):
    filter_type = CharFilter(method='filter_by_date_grouping')
    transaction_type = CharFilter(
        field_name='transaction_type', lookup_expr='exact')

    def filter_by_date_grouping(self, queryset, name, value):
        if value == 'daily':
            return queryset.annotate(period=TruncDate('created_at'))
        elif value == 'weekly':
            return queryset.annotate(period=TruncWeek('created_at'))
        elif value == 'monthly':
            return queryset.annotate(period=TruncMonth('created_at'))
        elif value == 'yearly':
            return queryset.annotate(period=TruncYear('created_at'))
        return queryset

    class Meta:
        model = FinanceRecord
        fields = ['filter_type', 'transaction_type']


class TransactionSummaryView(generics.ListAPIView):
    queryset = FinanceRecord.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionSummaryFilter

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        filter_type = request.query_params.get('filter_type', 'daily')
        transaction_type = request.query_params.get('transaction_type', 'all')

        # Apply date grouping first
        if filter_type == 'daily':
            queryset = queryset.annotate(period=TruncDate('created_at'))
        elif filter_type == 'weekly':
            queryset = queryset.annotate(period=TruncWeek('created_at'))
        elif filter_type == 'monthly':
            queryset = queryset.annotate(period=TruncMonth('created_at'))
        elif filter_type == 'yearly':
            queryset = queryset.annotate(period=TruncYear('created_at'))

        # Apply transaction type filter
        if transaction_type != 'all':
            queryset = queryset.filter(transaction_type=transaction_type)

        # Now group by period and calculate aggregates
        queryset = queryset.values('period').annotate(
            total_amount=Sum('amount'),
            count=Count('id')
        ).order_by('period')

        # Format the response
        response_data = {
            'filter': filter_type,
            'transaction_type': transaction_type,
            'summary': [
                {
                    'period': item['period'].strftime('%Y-%m-%d'),
                    'total_amount': float(item['total_amount']),
                    'count': item['count']
                }
                for item in queryset
            ]
        }

        return Response(response_data)
