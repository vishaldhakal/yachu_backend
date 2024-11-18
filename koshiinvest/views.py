from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Eventregistration
from .serializers import EventRegistrationSerializer

# Create your views here.

class EventRegistrationListCreateView(generics.ListCreateAPIView):
    queryset = Eventregistration.objects.all()
    serializer_class = EventRegistrationSerializer

class EventRegistrationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Eventregistration.objects.all()
    serializer_class = EventRegistrationSerializer
