from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post, Tag, Category, Author
from .serializers import PostCreateSerializer, PostSerializer, PostSmallSerializer, TagSerializer, CategorySerializer, TagSmallSerializer, CategorySmallSerializer, PostSlugSerializer, AuthorSerializer
from bs4 import BeautifulSoup
from about.models import Franchise
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters


class TagListCreateAPIView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'id'


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'


class AuthorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_queryset(self):
        franchise_slug = self.request.query_params.get('franchise')
        if franchise_slug:
            return Author.objects.filter(franchise__slug=franchise_slug)
        return Author.objects.all()

    def create(self, request, *args, **kwargs):
        franchise_slug = request.data.get('franchise')
        if franchise_slug:
            franchise = Franchise.objects.get(slug=franchise_slug)
            request.data['franchise'] = franchise
        return super().create(request, *args, **kwargs)


class AuthorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = 'id'


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSmallSerializer
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['created_at']

    def get_queryset(self):
        franchise_slug = self.request.query_params.get('franchise')
        if franchise_slug:
            return Post.objects.filter(franchise__slug=franchise_slug)
        return Post.objects.all()


@api_view(['POST'])
def post_create(request):
    if request.method == 'POST':
        # Handle the franchise data before passing to serializer
        data = request.data.copy()
        franchise_slug = data.get('franchise')

        # Handle the case where franchise_slug might be a list
        if isinstance(franchise_slug, list):
            franchise_slug = franchise_slug[0] if franchise_slug else None

        # Remove the franchise from data to avoid serializer validation error
        data.pop('franchise', None)

        serializer = PostCreateSerializer(data=data)
        if serializer.is_valid():
            # Get the franchise object after serializer validation
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


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'


@api_view(['GET'])
def post_list_slug(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSlugSerializer(posts, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def post_single(request, slug):
    if request.method == 'GET':
        posts = Post.objects.get(slug=slug)
        html_string = posts.blog_content
        soup = BeautifulSoup(html_string, 'html.parser')
        toc_div = soup.find('div', class_='mce-toc')
        if toc_div is not None:
            toc_div.extract()
        updated_html_string = str(toc_div)
        serializer = PostSerializer(posts)
        return Response({
            "data": serializer.data,
            "toc": updated_html_string,
        })


@api_view(['GET'])
def recent_posts(request):
    if request.method == 'GET':
        posts = Post.objects.all()[:5]
        posts_serializer = PostSerializer(posts, many=True)
        return Response({
            "recent_posts": posts_serializer.data,
        })
