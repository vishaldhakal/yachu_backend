from django.urls import path
from .views import ContactListCreateView

urlpatterns = [
    path('contacts/', ContactListCreateView.as_view(), name='contact-list-create'),
]