from django.shortcuts import render
from .models import Franchise
from .serializers import FranchiseSerializer
from rest_framework import generics


# Create your views here.
class FranchiseListCreateView(generics.ListCreateAPIView):
   queryset = Franchise.objects.all()
   serializer_class = FranchiseSerializer

class FranchiseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
   queryset = Franchise.objects.all()
   serializer_class = FranchiseSerializer