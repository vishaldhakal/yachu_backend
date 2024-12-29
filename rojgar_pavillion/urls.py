from django.urls import path
from .views import RegistrationView,AvailableSessionsView,TimeSlotByDateView

urlpatterns = [
    path('registrations/', RegistrationView.as_view(), name='registration-list'),
    path('registrations/available-sessions/', AvailableSessionsView.as_view(), name='available-sessions'),
    path('timeslots/', TimeSlotByDateView.as_view(), name='timeslot-by-date'),
]