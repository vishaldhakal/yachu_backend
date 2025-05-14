from django.urls import path
from .views import FinanceRecordDueDateView, FinanceRecordListCreateView, FinanceRecordDetailView

urlpatterns = [
    path('records/', FinanceRecordListCreateView.as_view(),
         name='finance-record-list-create'),
    path('records/<int:pk>/', FinanceRecordDetailView.as_view(),
         name='finance-record-detail'),
    path('records/due-date/', FinanceRecordDueDateView.as_view(),
         name='finance-record-due-date'),
]
