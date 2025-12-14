from django.urls import path

from . import views

urlpatterns = [
    # List all API keys or create a new one
    path("api-keys/", views.APIKeyListCreateView.as_view(), name="apikey-list-create"),
    # Retrieve, update, or delete a specific API key
    path(
        "api-keys/<int:pk>/",
        views.APIKeyRetrieveUpdateDestroyView.as_view(),
        name="apikey-detail",
    ),
    # Get the next rotated API key
    path("get-api-key/", views.get_rotated_key, name="get-rotated-key"),
]
