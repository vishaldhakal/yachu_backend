from rest_framework import generics

from .models import AIData
from .serializers import AIDataSerializer

# Create your views here.


class AIDataListCreateView(generics.ListCreateAPIView):
    queryset = AIData.objects.all()
    serializer_class = AIDataSerializer


class AIDataRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AIData.objects.all()
    serializer_class = AIDataSerializer
