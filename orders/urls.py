from django.urls import path
from . import views

urlpatterns = [
    path('sellers/', views.SellerListCreateView.as_view(), name='seller-list-create'),
    path('sellers/<int:pk>/', views.SellerRetrieveUpdateDestroyView.as_view(), name='seller-detail'),
    path('products/', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', views.ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),
    path('orders/', views.OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', views.OrderRetrieveUpdateDestroyView.as_view(), name='order-detail'),
    path('commissions/', views.CommissionListView.as_view(), name='commission-list'),
    path('commissions/<int:pk>/', views.CommissionRetrieveUpdateView.as_view(), name='commission-detail'),
]
