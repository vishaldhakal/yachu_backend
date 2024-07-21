from django.shortcuts import render
from .models import StallBooking
from .serializers import StallBookingSerializer,StallBookingSmallSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import json



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
   stall_type = request.GET.get('stall_type', None)
   if stall_type is not None:
      booked_stalls = StallBooking.objects.filter(status='Approved', stall_type=stall_type)
      pending_booked = StallBooking.objects.filter(status='Pending', stall_type=stall_type)
   else:
      booked_stalls = StallBooking.objects.filter(status='Approved')
      pending_booked = StallBooking.objects.filter(status='Pending')
   
   new_list = []
   for stall in booked_stalls:
      if stall.stall_no.__contains__(','):
         stall_no = stall.stall_no.split(',')
         new_listx = []
         for s in stall_no:
            new_listx.append(s)
            new_listx.append(stall.company)
         new_list.append(new_listx)
      else:
         new_listx = []
         new_listx.append(stall.stall_no)
         new_listx.append(stall.company)
         new_list.append(new_listx)

   #list to serialize
   """ new_list_json  = json.dumps(new_list) """
   
   new_list2 = []
   for stall in pending_booked:
      if stall.stall_no.__contains__(','):
         stall_no = stall.stall_no.split(',')
         for s in stall_no:
            new_list2.append(s)
      else:
         new_list2.append(stall.stall_no)

   #list to serialize
   """ new_list2_json  = json.dumps(new_list2) """

   serializer = StallBookingSmallSerializer(booked_stalls, many=True)
   serializer2 = StallBookingSmallSerializer(pending_booked, many=True) 
   return Response({"booked": serializer.data, "pending": serializer2.data, "stall_no_booked": new_list,"stall_no_pending": new_list2}, status=status.HTTP_200_OK)