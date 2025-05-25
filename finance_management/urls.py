from django.urls import path
from .views import FinanceRecordDueDateView, FinanceRecordListCreateView, FinanceRecordDetailView, FinanceRecordTotalView, TransactionSummaryView, FinanceRecordReminderView

urlpatterns = [
    path('records/', FinanceRecordListCreateView.as_view(),
         name='finance-record-list-create'),
    path('records/<int:pk>/', FinanceRecordDetailView.as_view(),
         name='finance-record-detail'),
    path('records/due-date/', FinanceRecordDueDateView.as_view(),
         name='finance-record-due-date'),
    path('records/total/', FinanceRecordTotalView.as_view(),
         name='finance-record-total'),
    path('summary/transactions/', TransactionSummaryView.as_view(),
         name='transaction-summary'),
    path('reminder/', FinanceRecordReminderView.as_view(),
         name='finance-record-reminder'),
]
