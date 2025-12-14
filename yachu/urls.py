from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("blog.urls")),
    path("api/", include("home.urls")),
    path("api/", include("about.urls")),
    path("api/", include("accounts.urls")),
    path("api/", include("orders.urls")),
    path("api/", include("finance_management.urls")),
    path("api/", include("contact.urls")),
    path("summernote/", include("django_summernote.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("tinymce/", include("tinymce.urls")),
    path("api/baliyo/", include("baliyo.urls")),
    path("api/", include("ai_data.urls")),
    path("api/", include("api_keys.urls")),  # API Key Rotation System
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
