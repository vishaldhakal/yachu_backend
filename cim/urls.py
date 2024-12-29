from django.urls import path
from . import views

urlpatterns = [
   path('stall/',views.StallBookingListCreateView.as_view(),name='stall-list-create'),
   path('export/',views.export,name='export'),
   path('stall/<int:pk>/',views.StallBookingRetrieveUpdateDestroyView.as_view(),name='stall-retrieve-update-destroy'),
   path("get-booked-stalls/", views.get_booked_stalls, name="get booked stalls"),
   path('approve-stall/<int:pk>/',views.approve_stall,name='approve stall'),
   path('reject-stall/<int:pk>/',views.reject_stall,name='reject stall'),
   path('sponsor/',views.SponsorBookingListCreateView.as_view(),name='sponsor-list-create'),
   path('sponsor/<int:pk>/',views.SponsorBookingRetrieveUpdateDestroyView.as_view(),name='sponsor-retrieve-update-destroy'),
]
