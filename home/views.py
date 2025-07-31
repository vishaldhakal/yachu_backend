from django.shortcuts import render, HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail, EmailMultiAlternatives
from datetime import datetime
from datetime import date

from about.models import Franchise
from .models import SiteConfiguration, FAQCategory, FAQ, Department, TeamMember, Testimonial, ImageGallery, VideoGallery, Banners, Product, FormData
from .serializers import SiteConfigurationSerializer, FAQCategorySerializer, FAQSerializer, DepartmentSerializer, TeamMemberSerializer, TestimonialSerializer, ImageGallerySerializer, VideoGallerySerializer, BannersSerializer, ProductSerializer, FormDataSerializer
from rest_framework import generics


@api_view(['POST'])
def send_email(request):
    data = request.data
    send_mail(data['subject'], data['message'],
              "info@yetihikes.com", ['vishaldhakal96@gmail.com'])
    return Response({'message': 'Email sent successfully'})


class SiteConfigurationListCreate(generics.ListCreateAPIView):
    queryset = SiteConfiguration.objects.all()
    serializer_class = SiteConfigurationSerializer


class SiteConfigurationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SiteConfiguration.objects.all()
    serializer_class = SiteConfigurationSerializer


class FAQCategoryListCreate(generics.ListCreateAPIView):
    queryset = FAQCategory.objects.all()
    serializer_class = FAQCategorySerializer


class FAQCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FAQCategory.objects.all()
    serializer_class = FAQCategorySerializer


class FAQListCreate(generics.ListCreateAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer


class FAQDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer


class DepartmentListCreate(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DepartmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class TeamMemberListCreate(generics.ListCreateAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer

    def get_queryset(self):
        franchise_slug = self.request.query_params.get('franchise')
        if franchise_slug:
            return TeamMember.objects.filter(franchise__slug=franchise_slug)
        return TeamMember.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        franchise_slug = data.get('franchise')

        if isinstance(franchise_slug, list):
            franchise_slug = franchise_slug[0] if franchise_slug else None

        data.pop('franchise', None)

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            if franchise_slug:
                try:
                    franchise = Franchise.objects.get(slug=franchise_slug)
                    serializer.save(franchise=franchise)
                except Franchise.DoesNotExist:
                    return Response({"error": "Franchise not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeamMemberDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer


class TestimonialListCreate(generics.ListCreateAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer


class TestimonialDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer


class ImageGalleryListCreate(generics.ListCreateAPIView):
    queryset = ImageGallery.objects.all()
    serializer_class = ImageGallerySerializer


class ImageGalleryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ImageGallery.objects.all()
    serializer_class = ImageGallerySerializer


class VideoGalleryListCreate(generics.ListCreateAPIView):
    queryset = VideoGallery.objects.all()
    serializer_class = VideoGallerySerializer


class VideoGalleryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = VideoGallery.objects.all()
    serializer_class = VideoGallerySerializer


class BannersListCreate(generics.ListCreateAPIView):
    queryset = Banners.objects.all()
    serializer_class = BannersSerializer


class BannersDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Banners.objects.all()
    serializer_class = BannersSerializer


class ProductListCreate(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class FormDataListCreateView(generics.ListCreateAPIView):
    queryset = FormData.objects.all()
    serializer_class = FormDataSerializer


class FormDataRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FormData.objects.all()
    serializer_class = FormDataSerializer
