from django.shortcuts import render,HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail, EmailMultiAlternatives
from datetime import datetime
from datetime import date
from .models import SiteConfiguration, FAQCategory, FAQ, Department, TeamMember, Testimonial, ImageGallery, VideoGallery,Banners,Product,FormData
from .serializers import SiteConfigurationSerializer, FAQCategorySerializer, FAQSerializer, DepartmentSerializer, TeamMemberSerializer, TestimonialSerializer, ImageGallerySerializer, VideoGallerySerializer,BannersSerializer,ProductSerializer,FormDataSerializer
from rest_framework import generics

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