from django.urls import path

from .views import PriceGuessListCreateAPIView, PriceGuessRetrieveUpdateDestroyAPIView

urlpatterns = [
    path(
        "price-guess/",
        PriceGuessListCreateAPIView.as_view(),
        name="price-guess-list-create",
    ),
    path(
        "price-guess/<int:pk>/",
        PriceGuessRetrieveUpdateDestroyAPIView.as_view(),
        name="price-guess-detail",
    ),
]
