from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from .filters import PriceGuessFilter
from .models import PriceGuess
from .serializers import PriceGuessSerializer


class PriceGuessListCreateAPIView(generics.ListCreateAPIView):
    """
    API view for listing all price guesses and creating new ones.
    GET: Returns a list of all price guesses
    POST: Creates a new price guess
    """

    queryset = PriceGuess.objects.all()
    serializer_class = PriceGuessSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PriceGuessFilter


class PriceGuessRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a specific price guess.
    GET: Returns a single price guess by ID
    PUT/PATCH: Updates a price guess
    DELETE: Deletes a price guess
    """

    queryset = PriceGuess.objects.all()
    serializer_class = PriceGuessSerializer
