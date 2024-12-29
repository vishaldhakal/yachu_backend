from django.shortcuts import render
from django.http import HttpResponse
from .models import StallBooking,SponsorBooking
from .serializers import StallBookingSerializer,StallBookingSmallSerializer,SponsorBookingSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import json
import csv


def export(request):
    getrec = StallBooking.objects.all()
    #csv
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="stallbooked.csv"'

    writer = csv.writer(response)
    writer.writerow(['stallno','company','phone','email','status','stalltype','total_amount','advance_amount','remaining_amount','amount_in_words','created_at','updated_at'])

    for rec in getrec:
        writer.writerow([rec.stall_no,rec.company,rec.phone,rec.email,rec.status,rec.stall_type,rec.total_amount,rec.advance_amount,rec.remaining_amount,rec.amount_in_words,rec.created_at,rec.updated_at])
        
    return response


class StallBookingListCreateView(generics.ListCreateAPIView):
   queryset = StallBooking.objects.all()
   serializer_class = StallBookingSerializer

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
         for s in stall_no:
            new_listx = []
            new_listx.append(s)
            new_listx.append(stall.company)
            new_listx.append(stall.status)
            new_list.append(new_listx)
      else:
         new_listx = []
         new_listx.append(stall.stall_no)
         new_listx.append(stall.company)
         new_listx.append(stall.status)
         new_list.append(new_listx)

   #list to serialize
   """ new_list_json  = json.dumps(new_list) """
   
   new_list2 = []
   for stall in pending_booked:
      if stall.stall_no.__contains__(','):
         stall_no = stall.stall_no.split(',')
         for s in stall_no:
            new_list2x = []
            new_list2x.append(s)
            new_list2x.append(stall.company)
            new_list2x.append(stall.status)
            new_list2.append(new_list2x)
      else:
         new_list2x = []
         new_list2x.append(stall.stall_no)
         new_list2x.append(stall.company)
         new_list2x.append(stall.status)
         new_list2.append(new_list2x)

   #list to serialize
   """ new_list2_json  = json.dumps(new_list2) """

   serializer = StallBookingSmallSerializer(booked_stalls, many=True)
   serializer2 = StallBookingSmallSerializer(pending_booked, many=True) 
   return Response({"booked": serializer.data, "pending": serializer2.data, "stall_no_booked": new_list,"stall_no_pending": new_list2}, status=status.HTTP_200_OK)


class SponsorBookingListCreateView(generics.ListCreateAPIView):
   queryset = SponsorBooking.objects.all()
   serializer_class = SponsorBookingSerializer

class SponsorBookingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
   queryset = SponsorBooking.objects.all()
   serializer_class = SponsorBookingSerializer