from datetime import datetime, timedelta
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, DateTimeFilter, CharFilter, DateFilter
from .models import FinanceRecord, Stock, Tag, Invoice
from .serializers import FinanceRecordBalanceSerializer, FinanceRecordListSerializer, FinanceRecordSerializer, InvoiceSmallSerializer, StockSerializer, TagSerializer, InvoiceSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth, TruncYear
from rest_framework.filters import SearchFilter
from django.db import models
from rest_framework.pagination import PageNumberPagination
from rest_framework import serializers
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

# Create your views here.


class TagFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')


class TagListCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TagFilter


class TagRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class FinanceRecordFilter(FilterSet):
    # Filter by date range
    organization = CharFilter(
        field_name='organization__id', lookup_expr='icontains')
    date_after = DateTimeFilter(field_name='created_at', lookup_expr='gte')
    date_before = DateTimeFilter(field_name='created_at', lookup_expr='lte')
    payment_method = CharFilter(
        field_name='payment_method', lookup_expr='icontains')
    transaction_type = CharFilter(
        field_name='transaction_type', lookup_expr='icontains')
    department = CharFilter(
        field_name='department__name', lookup_expr='icontains')
    date = DateFilter(field_name='created_at', lookup_expr='icontains')
    due_date = DateFilter(field_name='due_date', lookup_expr='icontains')

    class Meta:
        model = FinanceRecord
        fields = ['organization', 'transaction_type', 'department',
                  'date_after', 'date_before', 'payment_method', 'date', 'due_date']


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class FinanceRecordListCreateView(generics.ListCreateAPIView):
    queryset = FinanceRecord.objects.all().order_by('-created_at')
    serializer_class = FinanceRecordSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = FinanceRecordFilter
    search_fields = ['organization__name', 'transaction_type']
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FinanceRecordListSerializer
        return FinanceRecordSerializer

    def get_queryset(self):
        queryset = FinanceRecord.objects.all().order_by('-created_at')
        department_id = self.request.query_params.get('department_id')
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        return queryset

    def perform_create(self, serializer):
        # Automatically set the organization and user
        serializer.save()


class FinanceRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FinanceRecord.objects.all().order_by('-created_at')
    serializer_class = FinanceRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return FinanceRecordListSerializer
        return FinanceRecordSerializer

    def get_queryset(self):
        queryset = FinanceRecord.objects.all().order_by('-created_at')
        department_id = self.request.query_params.get('department_id')
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        return queryset


class FinanceRecordDueDateView(generics.ListAPIView):
    serializer_class = FinanceRecordListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Calculate the date 7 days from now
        date_limit = datetime.now() + timedelta(days=7)
        department_id = self.request.query_params.get('department_id')
        if department_id:
            return FinanceRecord.objects.filter(
                due_date__lte=date_limit,
                transaction_type__in=['Receivable', 'Payable'],
                department_id=department_id
            )
        return FinanceRecord.objects.filter(
            due_date__lte=date_limit,
            transaction_type__in=['Receivable', 'Payable']
        )


class FinanceRecordTotalView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        department_id = self.request.query_params.get('department_id')
        if department_id:
            totals = {
                'total_receivable': FinanceRecord.objects.filter(transaction_type='Receivable', department_id=department_id).aggregate(Sum('amount'))['amount__sum'] or 0,
                'total_payable': FinanceRecord.objects.filter(transaction_type='Payable', department_id=department_id).aggregate(Sum('amount'))['amount__sum'] or 0,
                'total_received': FinanceRecord.objects.filter(transaction_type='Received', department_id=department_id).aggregate(Sum('amount'))['amount__sum'] or 0,
                'total_paid': FinanceRecord.objects.filter(transaction_type='Paid', department_id=department_id).aggregate(Sum('amount'))['amount__sum'] or 0,
            }
        else:
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
        department_id = self.request.query_params.get('department_id')
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        filter_type = request.query_params.get('filter', 'daily')

        # Apply date grouping first
        if filter_type == 'daily':
            queryset = queryset.annotate(period=TruncDate('created_at'))
        elif filter_type == 'weekly':
            queryset = queryset.annotate(period=TruncWeek('created_at'))
        elif filter_type == 'monthly':
            queryset = queryset.annotate(period=TruncMonth('created_at'))
        elif filter_type == 'yearly':
            queryset = queryset.annotate(period=TruncYear('created_at'))

        # Now group by period and calculate money in/out
        queryset = queryset.values('period').annotate(
            money_in=Sum('amount', filter=models.Q(
                transaction_type='Received')),
            money_out=Sum('amount', filter=models.Q(transaction_type='Paid'))
        ).order_by('period')

        # Format the response
        response_data = {
            'filter': filter_type,
            'summary': [
                {
                    'period': item['period'].strftime('%Y-%m-%d'),
                    'money_in': float(item['money_in'] or 0),
                    'money_out': float(item['money_out'] or 0)
                }
                for item in queryset
            ]
        }

        return Response(response_data)


class FinanceRecordReminderView(generics.ListAPIView):
    serializer_class = FinanceRecordBalanceSerializer

    def get_queryset(self):
        # Calculate the date 7 days from now
        date_limit = datetime.now() + timedelta(days=7)
        department_id = self.request.query_params.get('department_id')
        if department_id:
            return FinanceRecord.objects.filter(
                due_date__lte=date_limit,
                transaction_type__in=['Receivable', 'Payable'],
                department_id=department_id
            ).order_by('due_date')
        return FinanceRecord.objects.filter(
            due_date__lte=date_limit,
            transaction_type__in=['Receivable', 'Payable']
            # Order by due date to show most urgent ones first
        ).order_by('due_date')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Add additional context about the reminder
        response_data = {
            'reminder_date': datetime.now().strftime('%Y-%m-%d'),
            'due_within_days': 7,
            'total_records': queryset.count(),
            'records': serializer.data
        }

        return Response(response_data)


class RecentRecordView(generics.ListAPIView):
    serializer_class = FinanceRecordListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        department_id = self.request.query_params.get('department_id')
        if department_id:
            return FinanceRecord.objects.filter(department_id=department_id).order_by('-created_at')[:10]
        return FinanceRecord.objects.all().order_by('-created_at')[:10]


class OrganizationTransactionSummaryView(generics.ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionSummaryFilter

    def list(self, request, organization_id, *args, **kwargs):
        queryset = FinanceRecord.objects.filter(
            organization_id=organization_id)
        department_id = self.request.query_params.get('department_id')
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        filter_type = request.query_params.get('filter', 'daily')

        # Apply date grouping
        if filter_type == 'daily':
            queryset = queryset.annotate(period=TruncDate('created_at'))
        elif filter_type == 'weekly':
            queryset = queryset.annotate(period=TruncWeek('created_at'))
        elif filter_type == 'monthly':
            queryset = queryset.annotate(period=TruncMonth('created_at'))
        elif filter_type == 'yearly':
            queryset = queryset.annotate(period=TruncYear('created_at'))

        # Group by period and calculate money in/out
        queryset = queryset.values('period').annotate(
            money_in=Sum('amount', filter=models.Q(
                transaction_type='Received')),
            money_out=Sum('amount', filter=models.Q(transaction_type='Paid'))
        ).order_by('period')

        # Format the response
        response_data = {
            'filter': filter_type,
            'summary': [
                {
                    'period': item['period'].strftime('%Y-%m-%d'),
                    'money_in': float(item['money_in'] or 0),
                    'money_out': float(item['money_out'] or 0)
                }
                for item in queryset
            ]
        }

        return Response(response_data)


class StockListCreateView(generics.ListCreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['product_name', 'product_code']

    def get_queryset(self):
        department_id = self.request.query_params.get('department_id')
        if department_id:
            return Stock.objects.filter(department_id=department_id)
        return Stock.objects.all()


class StockDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class OrganizationFinanceRecordReminderView(generics.ListAPIView):
    serializer_class = FinanceRecordBalanceSerializer

    def get_queryset(self):
        organization_id = self.kwargs.get('organization_id')
        # Calculate the date 7 days from now
        date_limit = datetime.now() + timedelta(days=7)
        department_id = self.request.query_params.get('department_id')
        if department_id:
            return FinanceRecord.objects.filter(
                organization_id=organization_id,
                due_date__lte=date_limit,
                transaction_type__in=['Receivable', 'Payable'],
                department_id=department_id
            ).order_by('due_date')
        return FinanceRecord.objects.filter(
            organization_id=organization_id,
            due_date__lte=date_limit,
            transaction_type__in=['Receivable', 'Payable']
        ).order_by('due_date')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Add additional context about the reminder
        response_data = {
            'reminder_date': datetime.now().strftime('%Y-%m-%d'),
            'due_within_days': 7,
            'total_records': queryset.count(),
            'records': serializer.data
        }

        return Response(response_data)


class InvoiceFilter(FilterSet):
    status = CharFilter(field_name='status', lookup_expr='icontains')
    start_date = DateFilter(method='filter_by_date')
    end_date = DateFilter(method='filter_by_date')

    def filter_by_date(self, queryset, name, value):
        if name == 'start_date':
            if not self.data.get('end_date'):
                # If only start_date is provided, use exact match
                return queryset.filter(invoice_date=value)
            else:
                # If both dates are provided, use range
                return queryset.filter(
                    invoice_date__gte=value,
                    invoice_date__lte=self.data.get('end_date')
                )
        return queryset

    class Meta:
        model = Invoice
        fields = ['status', 'start_date', 'end_date']


class InvoiceListCreateView(generics.ListCreateAPIView):
    queryset = Invoice.objects.all().order_by('-created_at')
    serializer_class = InvoiceSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    pagination_class = CustomPagination
    filterset_class = InvoiceFilter
    search_fields = ['invoice_number', 'bill_to_name']
    parser_classes = (JSONParser, FormParser, MultiPartParser)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return InvoiceSmallSerializer
        return InvoiceSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Handle both form-data and raw JSON formats
            data = request.data.copy()
            items = []

            # Check if items is already a list (JSON payload)
            if isinstance(request.data.get('items'), list):
                items = request.data.get('items')
            # Check if it's form-data format
            elif hasattr(request.data, 'getlist'):
                # Get the items string and convert it to list
                items_str = request.data.get('items')
                if items_str:
                    try:
                        import json
                        items = json.loads(items_str)
                    except json.JSONDecodeError:
                        return Response(
                            {"error": "Invalid items format"},
                            status=status.HTTP_400_BAD_REQUEST
                        )

            # Validate items
            if not items:
                return Response(
                    {"error": "At least one item is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create the modified data dictionary
            modified_data = {
                'bill_from_name': request.data.get('bill_from_name'),
                'bill_from_address': request.data.get('bill_from_address'),
                'bill_from_email': request.data.get('bill_from_email'),
                'bill_from_phone': request.data.get('bill_from_phone'),
                'bill_to_name': request.data.get('bill_to_name'),
                'bill_to_address': request.data.get('bill_to_address'),
                'bill_to_email': request.data.get('bill_to_email'),
                'bill_to_phone': request.data.get('bill_to_phone'),
                'invoice_number': request.data.get('invoice_number'),
                'invoice_date': request.data.get('invoice_date'),
                'due_date': request.data.get('due_date'),
                'currency': request.data.get('currency'),
                'discount': request.data.get('discount'),
                'discount_type': request.data.get('discount_type'),
                'vat': request.data.get('vat'),
                'total_amount': request.data.get('total_amount'),
                'additional_notes': request.data.get('additional_notes'),
                'payment_terms': request.data.get('payment_terms'),
                'bank_name': request.data.get('bank_name'),
                'account_name': request.data.get('account_name'),
                'account_number': request.data.get('account_number'),
                'status': request.data.get('status'),
                'items': items
            }

            # Handle logo file
            if 'logo' in request.FILES:
                modified_data['logo'] = request.FILES['logo']
            elif request.data.get('logo'):
                modified_data['logo'] = request.data.get('logo')

            # Handle signature file
            if 'signature' in request.FILES:
                modified_data['signature'] = request.FILES['signature']
            elif request.data.get('signature'):
                modified_data['signature'] = request.data.get('signature')

            # Update the request data
            request._full_data = modified_data

            # Call the parent create method
            return super().create(request, *args, **kwargs)
        except serializers.ValidationError as exc:
            return Response(exc.detail, status=status.HTTP_400_BAD_REQUEST)


class InvoiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    parser_classes = (JSONParser, FormParser, MultiPartParser)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return InvoiceSerializer
        return InvoiceSerializer

    def update(self, request, *args, **kwargs):
        try:
            # Handle both form-data and raw JSON formats
            data = request.data.copy()
            modified_data = {}

            # List of all possible fields
            fields = [
                'bill_from_name', 'bill_from_address', 'bill_from_email', 'bill_from_phone',
                'bill_to_name', 'bill_to_address', 'bill_to_email', 'bill_to_phone',
                'invoice_number', 'invoice_date', 'due_date', 'currency', 'discount',
                'discount_type', 'vat', 'total_amount', 'additional_notes', 'payment_terms',
                'bank_name', 'account_name', 'account_number', 'status'
            ]

            # Only include fields that are present in the request
            for field in fields:
                if field in request.data:
                    modified_data[field] = request.data.get(field)

            # Handle items separately
            items = []
            if isinstance(request.data.get('items'), list):
                items = request.data.get('items')
            elif hasattr(request.data, 'getlist'):
                items_str = request.data.get('items')
                if items_str:
                    try:
                        import json
                        items = json.loads(items_str)
                        modified_data['items'] = items
                    except json.JSONDecodeError:
                        return Response(
                            {"error": "Invalid items format"},
                            status=status.HTTP_400_BAD_REQUEST
                        )

            # Handle file uploads
            if 'logo' in request.FILES:
                modified_data['logo'] = request.FILES['logo']
            elif request.data.get('logo'):
                modified_data['logo'] = request.data.get('logo')

            if 'signature' in request.FILES:
                modified_data['signature'] = request.FILES['signature']
            elif request.data.get('signature'):
                modified_data['signature'] = request.data.get('signature')

            # Update the request data
            request._full_data = modified_data

            # Call the parent update method
            return super().update(request, *args, **kwargs)
        except serializers.ValidationError as exc:
            return Response(exc.detail, status=status.HTTP_400_BAD_REQUEST)


class InvoiceStatisticsView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        base_queryset = Invoice.objects.all()

        # Calculate statistics for each status
        statistics = {
            'total': {
                'count': base_queryset.count(),
                'amount': float(base_queryset.aggregate(Sum('total_amount'))['total_amount__sum'] or 0)
            },
            'paid': {
                'count': base_queryset.filter(status='Paid').count(),
                'amount': float(base_queryset.filter(status='Paid').aggregate(Sum('total_amount'))['total_amount__sum'] or 0)
            },
            'pending': {
                'count': base_queryset.filter(status='Pending').count(),
                'amount': float(base_queryset.filter(status='Pending').aggregate(Sum('total_amount'))['total_amount__sum'] or 0)
            },
            'overdue': {
                'count': base_queryset.filter(status='Overdue').count(),
                'amount': float(base_queryset.filter(status='Overdue').aggregate(Sum('total_amount'))['total_amount__sum'] or 0)
            },
            'draft': {
                'count': base_queryset.filter(status='Draft').count(),
                'amount': float(base_queryset.filter(status='Draft').aggregate(Sum('total_amount'))['total_amount__sum'] or 0)
            }
        }

        return Response(statistics, status=status.HTTP_200_OK)
