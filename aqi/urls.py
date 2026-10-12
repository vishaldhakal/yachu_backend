from django.urls import path

from .views import (
    AQIListCreateAPIView,
    LatestAQIAPIView,
)

urlpatterns = [
    path("aqi/", AQIListCreateAPIView.as_view(), name="aqi-list-create"),
    path("aqi/latest/", LatestAQIAPIView.as_view(), name="aqi-latest"),
]
