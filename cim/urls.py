from django.urls import path
from . import views

urlpatterns = [
   path('stall/',views.StallBookingListCreateView.as_view(),name='stall-list-create'),
   path('stall/<int:pk>/',views.StallBookingRetrieveUpdateDestroyView.as_view(),name='stall-retrieve-update-destroy'),
   path('approve-stall/<int:pk>/',views.approve_stall,name='approve stall'),
   path('reject-stall/<int:pk>/',views.reject_stall,name='reject stall'),
]
