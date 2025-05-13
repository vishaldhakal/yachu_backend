from django.urls import path
from .views import RegisterView, LoginView, OrganizationListCreateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('organizations/', OrganizationListCreateView.as_view(),
         name='organization-list-create'),
]
