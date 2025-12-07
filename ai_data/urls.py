from django.urls import path

from .views import AIDataListCreateView, AIDataRetrieveUpdateDestroyView

urlpatterns = [
    path("ai-data/", AIDataListCreateView.as_view(), name="ai-data-list-create"),
    path(
        "ai-data/<int:pk>/",
        AIDataRetrieveUpdateDestroyView.as_view(),
        name="ai-data-retrieve-update-destroy",
    ),
]
