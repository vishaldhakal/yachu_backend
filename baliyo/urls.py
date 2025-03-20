from django.urls import path
from . import views

urlpatterns = [
    # Service URLs
    path('services/', views.ServiceListCreateView.as_view(), name='service-list-create'),
    path('services/<slug:slug>/', views.ServiceDetailView.as_view(), name='service-detail'),

    # Image URLs
    path('images/', views.ImageListCreateView.as_view(), name='image-list-create'),
    path('images/<int:pk>/', views.ImageDetailView.as_view(), name='image-detail'),

    # Project URLs
    path('projects/', views.ProjectListCreateView.as_view(), name='project-list-create'),
    path('projects/<slug:slug>/', views.ProjectDetailView.as_view(), name='project-detail'),

    # Blog Category URLs
    path('blog-categories/', views.BlogCategoryListCreateView.as_view(), name='blog-category-list-create'),
    path('blog-categories/<slug:slug>/', views.BlogCategoryDetailView.as_view(), name='blog-category-detail'),

    # Blog Tag URLs
    path('blog-tags/', views.BlogTagListCreateView.as_view(), name='blog-tag-list-create'),
    path('blog-tags/<int:pk>/', views.BlogTagDetailView.as_view(), name='blog-tag-detail'),

    # Blog URLs
    path('blogs/', views.BlogListCreateView.as_view(), name='blog-list-create'),
    path('blogs/<slug:slug>/', views.BlogDetailView.as_view(), name='blog-detail'),

    # Contact URLs
    path('contacts/', views.ContactListCreateView.as_view(), name='contact-list-create'),
    path('contacts/<int:pk>/', views.ContactDetailView.as_view(), name='contact-detail'),

    # TeamMember URLs
    path('team-members/', views.TeamMemberListCreateView.as_view(), name='team-member-list-create'),
    path('team-members/<int:pk>/', views.TeamMemberDetailView.as_view(), name='team-member-detail'),

    # FAQ URLs
    path('faqs/', views.FaqListCreateView.as_view(), name='faq-list-create'),
    path('faqs/<int:pk>/', views.FaqDetailView.as_view(), name='faq-detail'),

    # Testimonial URLs
    path('testimonials/', views.TestimonialListCreateView.as_view(), name='testimonial-list-create'),
    path('testimonials/<int:pk>/', views.TestimonialDetailView.as_view(), name='testimonial-detail'),
]

