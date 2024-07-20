from django.urls import path
from . import views

urlpatterns = [
   path('franchise/',views.StallBookingListCreateView.as_view(),name='stall-list-create'),
   path('franchise/<int:pk>/',views.StallBookingRetrieveUpdateDestroyView.as_view(),name='stall-retrieve-update-destroy'),
]
