from .models import SiteConfiguration, FAQCategory, FAQ, Department, TeamMember, Testimonial, ImageGallery, VideoGallery,Banners
from rest_framework import serializers

class SiteConfigurationSerializer(serializers.ModelSerializer):
   class Meta:
      model = SiteConfiguration
      fields = '__all__'
      depth = 2

class FAQCategorySerializer(serializers.ModelSerializer):
   class Meta:
      model = FAQCategory
      fields = '__all__'
      depth = 2

class FAQSerializer(serializers.ModelSerializer):
   class Meta:
      model = FAQ
      fields = '__all__'
      depth = 2

class DepartmentSerializer(serializers.ModelSerializer):
   class Meta:
      model = Department
      fields = '__all__'
      depth = 2

class TeamMemberSerializer(serializers.ModelSerializer):
   class Meta:
      model = TeamMember
      fields = '__all__'
      depth = 2

class TestimonialSerializer(serializers.ModelSerializer):
   class Meta:
      model = Testimonial
      fields = '__all__'
      depth = 2

class ImageGallerySerializer(serializers.ModelSerializer):
   class Meta:
      model = ImageGallery
      fields = '__all__'
      depth = 2

class VideoGallerySerializer(serializers.ModelSerializer):

   class Meta:
      model = VideoGallery
      fields = '__all__'
      depth = 2

class BannersSerializer(serializers.ModelSerializer):
   class Meta:
      model = Banners
      fields = '__all__'
      depth = 2
