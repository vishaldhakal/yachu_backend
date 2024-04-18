from django.urls import path, include
#import views from views.py file 
from . import views

urlpatterns = [
   path('site-configs/', views.SiteConfigurationListCreate.as_view(), name='site_configs'),
   path('site-configs/<int:pk>/', views.SiteConfigurationDetail.as_view(), name='site_config_detail'),
   path('faq-categories/', views.FAQCategoryListCreate.as_view(), name='faq_categories'),
   path('faq-categories/<int:pk>/', views.FAQCategoryDetail.as_view(), name='faq_category_detail'),
   path('faqs/', views.FAQListCreate.as_view(), name='faqs'),
   path('faqs/<int:pk>/', views.FAQDetail.as_view(), name='faq_detail'),
   path('departments/', views.DepartmentListCreate.as_view(), name='departments'),
   path('departments/<int:pk>/', views.DepartmentDetail.as_view(), name='department_detail'),
   path('team-members/', views.TeamMemberListCreate.as_view(), name='team_members'),
   path('team-members/<int:pk>/', views.TeamMemberDetail.as_view(), name='team_member_detail'),
   path('testimonials/', views.TestimonialListCreate.as_view(), name='testimonials'),
   path('testimonials/<int:pk>/', views.TestimonialDetail.as_view(), name='testimonial_detail'),
   path('image-galleries/', views.ImageGalleryListCreate.as_view(), name='image_galleries'),
   path('image-galleries/<int:pk>/', views.ImageGalleryDetail.as_view(), name='image_gallery_detail'),
   path('video-galleries/', views.VideoGalleryListCreate.as_view(), name='video_galleries'),
   path('video-galleries/<int:pk>/', views.VideoGalleryDetail.as_view(), name='video_gallery_detail'),
   path('banners/', views.BannersListCreate.as_view(), name='banners'),
   path('banners/<int:pk>/', views.BannersDetail.as_view(), name='banner_detail'),
]
