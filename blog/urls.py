from django.urls import path
from .views import AuthorListCreateAPIView, AuthorRetrieveUpdateDestroyAPIView, CategoryListCreateAPIView, CategoryRetrieveUpdateDestroyAPIView, PostListAPIView, TagListCreateAPIView, TagRetrieveUpdateDestroyAPIView, post_single, post_list_slug, recent_posts, post_create, PostRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('posts/', PostListAPIView.as_view(), name='post_list'),
    path('posts/create/', post_create, name='post_create'),
    path('latest-posts/', recent_posts, name='recent_posts'),
    path('posts-slug/', post_list_slug, name='post_list_slug'),
    path('post-single/<str:slug>/', post_single, name='post_single'),
    path('posts/<str:slug>/',
         PostRetrieveUpdateDestroyAPIView.as_view(), name='post-detail'),
    path('tags/', TagListCreateAPIView.as_view(), name='tag_list'),
    path('tags/<int:id>/', TagRetrieveUpdateDestroyAPIView.as_view(), name='tag_detail'),
    path('categories/', CategoryListCreateAPIView.as_view(), name='category_list'),
    path('categories/<int:id>/',
         CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category_detail'),
    path('authors/', AuthorListCreateAPIView.as_view(), name='author_list'),
    path('authors/<int:id>/',
         AuthorRetrieveUpdateDestroyAPIView.as_view(), name='author_detail'),
]
