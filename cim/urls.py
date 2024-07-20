from django.urls import path
from . import views

urlpatterns = [
   path('stall/',views.StallBookingListCreateView.as_view(),name='stall-list-create'),
   path('stall/<int:pk>/',views.StallBookingRetrieveUpdateDestroyView.as_view(),name='stall-retrieve-update-destroy'),
]
