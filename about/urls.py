from django.urls import path, include
from . import views

urlpatterns = [
   path('franchise/',views.FranchiseListCreateView.as_view(),name='franchise-list-create'),
   path('franchise/<int:pk>/',views.FranchiseRetrieveUpdateDestroyView.as_view(),name='franchise-retrieve-update-destroy'),
]
