from django.shortcuts import render
from .models import StallBooking
from .serializers import StallBookingSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view



class StallBookingListCreateView(generics.ListCreateAPIView):
   queryset = StallBooking.objects.all()
   serializer_class = StallBookingSerializer

   def list(self, request, *args, **kwargs):
      status = request.get.GET('status', None)
      advance_paid = request.get.GET('advance_paid', None)
      
      if advance_paid is not None:
         queryset = StallBooking.objects.filter(remaining_amount=0)
      else:
         queryset = StallBooking.objects.all()

      if status is not None:
         queryset = queryset.filter(status=status)

      serializer = StallBookingSerializer(queryset, many=True)
      return Response(serializer.data)

class StallBookingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
   queryset = StallBooking.objects.all()
   serializer_class = StallBookingSerializer

@api_view(['POST'])
def approve_stall(request, pk):
   stall = StallBooking.objects.get(pk=pk)
   stall.status = 'Approved'
   stall.save()
   return Response({'message': 'Stall Approved', 'status': status.HTTP_200_OK})

@api_view(['POST'])
def reject_stall(request, pk):
   stall = StallBooking.objects.get(pk=pk)
   stall.status = 'Rejected'
   stall.save()
   return Response({'message': 'Stall Rejected', 'status': status.HTTP_200_OK})

@api_view(['GET'])
def get_booked_stalls(request):
   booked_stalls = StallBooking.objects.filter(status='Approved')
   pending_booked = StallBooking.objects.filter(status='Pending')

   serializer = StallBookingSerializer(booked_stalls, many=True)
   serializer2 = StallBookingSerializer(pending_booked, many=True) 
   return Response({"booked": serializer.data, "pending": serializer2.data})