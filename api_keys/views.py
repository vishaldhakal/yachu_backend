from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import APIKey
from .serializers import APIKeySerializer, APIKeyUsageSerializer


class APIKeyListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating API keys.

    GET: List all API keys (optionally filter by is_active)
    POST: Create a new API key
    """

    queryset = APIKey.objects.all()
    serializer_class = APIKeySerializer

    def get_queryset(self):
        """Optionally filter by is_active status."""
        queryset = APIKey.objects.all()
        is_active = self.request.query_params.get("is_active", None)

        if is_active is not None:
            is_active_bool = is_active.lower() in ["true", "1", "yes"]
            queryset = queryset.filter(is_active=is_active_bool)

        return queryset.order_by("-created_at")


class APIKeyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a specific API key.

    GET: Retrieve a specific API key
    PUT/PATCH: Update a specific API key
    DELETE: Delete a specific API key
    """

    queryset = APIKey.objects.all()
    serializer_class = APIKeySerializer


@api_view(["GET"])
def get_rotated_key(request):
    """
    Get the next API key in rotation.
    Automatically increments usage count and updates last_used_at timestamp.
    Returns 404 if no active keys are available.
    """
    api_key = APIKey.get_next_key()

    if not api_key:
        return Response(
            {"error": "No active API keys available"}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = APIKeyUsageSerializer(api_key)
    return Response(serializer.data, status=status.HTTP_200_OK)
