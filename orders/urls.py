from django.urls import path
from .views import OrderListCreateView, OrderRetrieveUpdateDeleteView

urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderRetrieveUpdateDeleteView.as_view(), name='order-detail'),
]
