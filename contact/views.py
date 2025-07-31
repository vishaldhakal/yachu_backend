from warnings import filters
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from .models import Contact
from .serializers import ContactSerializer
from about.models import Franchise
from blog.views import CustomPagination
# Create your views here.


class ContactListCreateView(ListCreateAPIView):
    queryset = Contact.objects.all().order_by('-created_at')
    serializer_class = ContactSerializer
    pagination_class = CustomPagination
    search_fields = ['name']

    def get_queryset(self):
        franchise_slug = self.request.query_params.get('franchise')
        if franchise_slug:
            return Contact.objects.filter(franchise__slug=franchise_slug).order_by('-created_at')
        return Contact.objects.all().order_by('-created_at')

    def create(self, request, *args, **kwargs):
        franchise_slug = request.data.get('franchise')
        if franchise_slug:
            franchise = Franchise.objects.get(slug=franchise_slug)
            request.data['franchise'] = franchise.id
        return super().create(request, *args, **kwargs)
