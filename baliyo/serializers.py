from rest_framework import serializers
from .models import Service, Image, Project, Blog, Contact, TeamMember, Faq, Testimonial, BlogCategory, BlogTag, OurPartner


class ProjectSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'slug', 'thumbnail_image',
                  'thumbnail_image_alt_description', 'meta_description', 'meta_title']


class ServiceSerializer(serializers.ModelSerializer):
    projects = ProjectSmallSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        # fields = '__all__'
        exclude = ['created_at', 'updated_at']


class ServiceSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'title', 'slug', 'icon', 'thumbnail_image',
                  'thumbnail_image_alt_description', 'short_description']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'


class BlogTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = '__all__'


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):
    category = BlogCategorySerializer(read_only=True)
    tags = BlogTagSerializer(many=True, read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=BlogCategory.objects.all(),
        source='category',
        write_only=True
    )
    tag_id = serializers.PrimaryKeyRelatedField(
        queryset=BlogTag.objects.all(),
        source='tags',
        write_only=True,
        many=True,
        required=False
    )

    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug', 'description', 'thumbnail_image',
                  'thumbnail_image_alt_description', 'category', 'category_id',
                  'tags', 'tag_id', 'created_at', 'updated_at']


class BlogSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug', 'thumbnail_image',
                  'thumbnail_image_alt_description', 'meta_title', 'meta_description']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = '__all__'


class TeamMemberSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ['id', 'name', 'designation',
                  'image', 'image_alt_description']


class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = '__all__'


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'


class TestimonialSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['id', 'name', 'message', 'rating',
                  'designation', 'image', 'image_alt_description']


class OurPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OurPartner
        fields = '__all__'
