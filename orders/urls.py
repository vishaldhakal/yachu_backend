from django.urls import path
from .views import OrderListCreateView
urlpatterns = [
    path('order/', OrderListCreateView.as_view(), name='order'),
]
