from rest_framework import serializers
from .models import Service, Image, Project, Blog, Contact, TeamMember, Faq, Testimonial, BlogCategory, BlogTag

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

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
    tag_ids = serializers.PrimaryKeyRelatedField(
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
                 'tags', 'tag_ids', 'created_at', 'updated_at']

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = '__all__'

class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = '__all__'

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'
