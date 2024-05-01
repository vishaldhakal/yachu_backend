from .models import SiteConfiguration, FAQCategory, FAQ, Department, TeamMember, Testimonial, ImageGallery, VideoGallery,Banners,Product,Member,FileSchema,FormData
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

class ProductSerializer(serializers.ModelSerializer):
   class Meta:
      model = Product
      fields = '__all__'
      depth = 2


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'name', 'email']

class FileSchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileSchema
        fields = ['id', 'file']

class FormDataSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True)
    robot_photos = FileSchemaSerializer(many=True, required=False)

    class Meta:
        model = FormData
        fields = ['id', 'team_name', 'team_description', 'members', 'robot_name', 'robot_description', 'robot_photos']

    def create(self, validated_data):
        members_data = validated_data.pop('members')
        robot_photos_data = validated_data.pop('robot_photos', [])

        form_data = FormData.objects.create(**validated_data)

        for member_data in members_data:
            member, _ = Member.objects.get_or_create(**member_data)
            form_data.members.add(member)

        for photo_data in robot_photos_data:
            photo, _ = FileSchema.objects.get_or_create(**photo_data)
            form_data.robot_photos.add(photo)

        return form_data