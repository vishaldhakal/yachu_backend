from django.urls import path

from . import views

urlpatterns = [
    # Service URLs
    path(
        "services/", views.ServiceListCreateView.as_view(), name="service-list-create"
    ),
    path(
        "services/<slug:slug>/",
        views.ServiceDetailView.as_view(),
        name="service-detail",
    ),
    # Image URLs
    path("images/", views.ImageListCreateView.as_view(), name="image-list-create"),
    path("images/<int:pk>/", views.ImageDetailView.as_view(), name="image-detail"),
    # Project URLs
    path(
        "projects/", views.ProjectListCreateView.as_view(), name="project-list-create"
    ),
    path(
        "projects/<slug:slug>/",
        views.ProjectDetailView.as_view(),
        name="project-detail",
    ),
    # Project Demo URLs
    path(
        "project-demos/",
        views.ProjectDemoListCreateView.as_view(),
        name="project-demo-list-create",
    ),
    path(
        "project-demos/<int:pk>/",
        views.ProjectDemoDetailView.as_view(),
        name="project-demo-detail",
    ),
    # Technical Document URLs
    path(
        "technical-documents/",
        views.TechnicalDocumentListCreateView.as_view(),
        name="technical-document-list-create",
    ),
    path(
        "technical-documents/<int:pk>/",
        views.TechnicalDocumentDetailView.as_view(),
        name="technical-document-detail",
    ),
    # Blog Category URLs
    path(
        "blog-categories/",
        views.BlogCategoryListCreateView.as_view(),
        name="blog-category-list-create",
    ),
    path(
        "blog-categories/<slug:slug>/",
        views.BlogCategoryDetailView.as_view(),
        name="blog-category-detail",
    ),
    # Blog Tag URLs
    path(
        "blog-tags/", views.BlogTagListCreateView.as_view(), name="blog-tag-list-create"
    ),
    path(
        "blog-tags/<int:pk>/", views.BlogTagDetailView.as_view(), name="blog-tag-detail"
    ),
    # Blog URLs
    path("blogs/", views.BlogListCreateView.as_view(), name="blog-list-create"),
    path("blogs/<slug:slug>/", views.BlogDetailView.as_view(), name="blog-detail"),
    # Contact URLs
    path(
        "contacts/", views.ContactListCreateView.as_view(), name="contact-list-create"
    ),
    path(
        "contacts/<int:pk>/", views.ContactDetailView.as_view(), name="contact-detail"
    ),
    # TeamMember URLs
    path(
        "team-members/",
        views.TeamMemberListCreateView.as_view(),
        name="team-member-list-create",
    ),
    path(
        "team-members/<int:pk>/",
        views.TeamMemberDetailView.as_view(),
        name="team-member-detail",
    ),
    # FAQ URLs
    path("faqs/", views.FaqListCreateView.as_view(), name="faq-list-create"),
    path("faqs/<int:pk>/", views.FaqDetailView.as_view(), name="faq-detail"),
    # Testimonial URLs
    path(
        "testimonials/",
        views.TestimonialListCreateView.as_view(),
        name="testimonial-list-create",
    ),
    path(
        "testimonials/<int:pk>/",
        views.TestimonialDetailView.as_view(),
        name="testimonial-detail",
    ),
    # OurPartner URLs
    path(
        "our-partners/",
        views.OurPartnerListCreateView.as_view(),
        name="our-partner-list-create",
    ),
    path(
        "our-partners/<int:pk>/",
        views.OurPartnerDetailView.as_view(),
        name="our-partner-detail",
    ),
    # Gallery URLs
    path("gallery/", views.GalleryListCreateView.as_view(), name="gallery-list-create"),
    path("gallery/<int:pk>/", views.GalleryDetailView.as_view(), name="gallery-detail"),
    # LeaveForm URLs
    path(
        "leave-forms/",
        views.LeaveFormListCreateView.as_view(),
        name="leave-form-list-create",
    ),
    path(
        "leave-forms/<int:pk>/",
        views.LeaveFormDetailView.as_view(),
        name="leave-form-detail",
    ),
    # Vendor URLs
    path("vendors/", views.VendorListCreateView.as_view(), name="vendor-list-create"),
    path(
        "vendors/<slug:slug>/", views.VendorDetailView.as_view(), name="vendor-detail"
    ),
    # Project Tool URLs
    path(
        "project-tools/",
        views.ProjectToolListCreateView.as_view(),
        name="project-tool-list-create",
    ),
    path(
        "project-tools/<slug:slug>/",
        views.ProjectToolDetailView.as_view(),
        name="project-tool-detail",
    ),
    # Component URLs
    path(
        "components/",
        views.ComponentListCreateView.as_view(),
        name="component-list-create",
    ),
    path(
        "components/<slug:slug>/",
        views.ComponentDetailView.as_view(),
        name="component-detail",
    ),
    # Component Model URLs
    path(
        "component-models/",
        views.ComponentModelListCreateView.as_view(),
        name="component-model-list-create",
    ),
    path(
        "component-models/<slug:slug>/",
        views.ComponentModelDetailView.as_view(),
        name="component-model-detail",
    ),
    # Component Purchase URLs
    path(
        "component-purchases/",
        views.ComponentPurchaseListCreateView.as_view(),
        name="component-purchase-list-create",
    ),
    path(
        "component-purchases/<int:pk>/",
        views.ComponentPurchaseDetailView.as_view(),
        name="component-purchase-detail",
    ),
    # Inventory URLs
    path(
        "inventory/",
        views.InventoryListCreateView.as_view(),
        name="inventory-list-create",
    ),
    path(
        "inventory/<int:pk>/",
        views.InventoryDetailView.as_view(),
        name="inventory-detail",
    ),
    # Project Inventory Used URLs
    path(
        "project-inventory-used/",
        views.ProjectInventoryUsedListCreateView.as_view(),
        name="project-inventory-used-list-create",
    ),
    path(
        "project-inventory-used/<int:pk>/",
        views.ProjectInventoryUsedDetailView.as_view(),
        name="project-inventory-used-detail",
    ),
    # Project Daily Update URLs
    path(
        "project-daily-updates/",
        views.ProjectDailyUpdateListCreateView.as_view(),
        name="project-daily-update-list-create",
    ),
    path(
        "project-daily-updates/<int:pk>/",
        views.ProjectDailyUpdateDetailView.as_view(),
        name="project-daily-update-detail",
    ),
]
