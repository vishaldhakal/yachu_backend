from django.urls import path
from .views import RegisterView, LoginView, OrganizationListCreateView, OrganizationDetailView, DepartmentListCreateView, DepartmentDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('organizations/', OrganizationListCreateView.as_view(),
         name='organization-list-create'),
    path('organizations/<int:pk>/', OrganizationDetailView.as_view(),
         name='organization-detail'),
    path('finance-departments/', DepartmentListCreateView.as_view(),
         name='department-list-create'),
    path('finance-departments/<int:pk>/', DepartmentDetailView.as_view(),
         name='department-detail'),

]
