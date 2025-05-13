from django.urls import path
from .views import FinanceRecordListCreateView, FinanceRecordDetailView

urlpatterns = [
    path('records/', FinanceRecordListCreateView.as_view(),
         name='finance-record-list-create'),
    path('records/<int:pk>/', FinanceRecordDetailView.as_view(),
         name='finance-record-detail'),
]
