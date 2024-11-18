from django.urls import path
from .views import EventRegistrationListCreateView, EventRegistrationDetailView

urlpatterns = [
    path('event-registrations/', 
         EventRegistrationListCreateView.as_view(), 
         name='event-registration-list'),
    path('event-registrations/<int:pk>/', 
         EventRegistrationDetailView.as_view(), 
         name='event-registration-detail'),
] 