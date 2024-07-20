from django.shortcuts import render
from .models import StallBooking
from .serializers import StallBookingSerializer
from rest_framework import generics


class StallBookingListCreateView(generics.ListCreateAPIView):
   queryset = StallBooking.objects.all()
   serializer_class = StallBookingSerializer

class StallBookingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
   queryset = StallBooking.objects.all()
   serializer_class = StallBookingSerializer