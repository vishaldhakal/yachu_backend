import os

import resend
from django.template.loader import render_to_string
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Blog,
    BlogCategory,
    BlogTag,
    Contact,
    Faq,
    Gallery,
    Image,
    LeaveForm,
    OurPartner,
    Project,
    ProjectDemo,
    ProjectRenderingImage,
    Service,
    TeamMember,
    Testimonial,
)
from .serializers import (
    BlogCategorySerializer,
    BlogSerializer,
    BlogSmallSerializer,
    BlogTagSerializer,
    ContactSerializer,
    FaqSerializer,
    GallerySerializer,
    GallerySmallSerializer,
    ImageSerializer,
    LeaveFormSerializer,
    OurPartnerSerializer,
    ProjectDemoSerializer,
    ProjectRenderingImageSerializer,
    ProjectSerializer,
    ProjectSmallSerializer,
    ServiceSerializer,
    ServiceSmallSerializer,
    TeamMemberSerializer,
    TeamMemberSmallSerializer,
    TestimonialSerializer,
    TestimonialSmallSerializer,
)

# Configure Resend with API key from settings
resend.api_key = os.getenv("RESEND_API_KEY")

# Create your views here.


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


# Service Views


class ServiceListCreateView(generics.ListCreateAPIView):
    queryset = Service.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ServiceSmallSerializer
        return ServiceSerializer


class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    lookup_field = "slug"


# Image Views


class ImageListCreateView(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class ImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


# Project Views


class ProjectListCreateView(generics.ListCreateAPIView):
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Project.objects.all().order_by("-created_at")
        category_slug = self.request.query_params.get("category", None)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProjectSmallSerializer
        return ProjectSerializer


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all().prefetch_related(
        "images", "category", "demos", "rendering_images"
    )
    serializer_class = ProjectSerializer
    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Get similar projects from same category
        similar_projects = (
            Project.objects
            .filter(category__in=instance.category.all())
            .exclude(id=instance.id)
            .distinct()[:3]
        )

        # Serialize similar projects
        similar_projects_data = ProjectSmallSerializer(similar_projects, many=True).data

        # Combine the data
        response_data = serializer.data
        response_data["similar_projects"] = similar_projects_data

        return Response(response_data)


# ProjectDemo Views


class ProjectDemoListCreateView(generics.ListCreateAPIView):
    queryset = ProjectDemo.objects.all().select_related("project")
    serializer_class = ProjectDemoSerializer


class ProjectDemoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProjectDemo.objects.all().select_related("project")
    serializer_class = ProjectDemoSerializer


# ProjectRenderingImage Views


class ProjectRenderingImageListCreateView(generics.ListCreateAPIView):
    queryset = ProjectRenderingImage.objects.all().select_related("project")
    serializer_class = ProjectRenderingImageSerializer


class ProjectRenderingImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProjectRenderingImage.objects.all().select_related("project")
    serializer_class = ProjectRenderingImageSerializer


# Blog Views


class BlogListCreateView(generics.ListCreateAPIView):
    queryset = Blog.objects.all().order_by("-created_at")
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BlogSmallSerializer
        return BlogSerializer


class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = "slug"


# Contact Views


class ContactListCreateView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def get_queryset(self):
        queryset = Contact.objects.all()
        company_name = self.request.query_params.get("company", None)
        if company_name:
            queryset = queryset.filter(company=company_name)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            contact = serializer.save()

            # Prepare email context
            context = {
                "name": contact.name,
                "email": contact.email,
                "phone": contact.phone or "Not provided",
                "company": contact.company or "baliyoventures",
                "message": contact.message,
                "date": contact.created_at.strftime("%B %d, %Y"),
                "time": contact.created_at.strftime("%I:%M %p"),
            }

            # Render email template
            html_message = render_to_string("emails/contact_notification.html", context)

            try:
                # Determine recipient based on company
                company_name = contact.company.lower() if contact.company else ""
                if "baliyotechnologies" in company_name:
                    to_email = "baliyotechnologies@gmail.com"
                else:
                    to_email = "baliyoventures@gmail.com"

                # Send email using Resend
                params = {
                    "from": "Baliyo Contact Form <contact@baliyoventures.com>",
                    "to": [to_email],
                    "subject": f"New Contact Form Submission from {contact.name}",
                    "html": html_message,
                    "reply_to": contact.email,
                }

                resend.Emails.send(params)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            except Exception as e:
                # Log the error and still return success to the user
                print(f"Error sending email via Resend: {str(e)}")
                return Response(
                    {
                        "detail": "Contact form submitted but there was an error sending the notification."
                    },
                    status=status.HTTP_201_CREATED,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


# TeamMember Views


class TeamMemberListCreateView(generics.ListCreateAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TeamMemberSmallSerializer
        return TeamMemberSerializer


class TeamMemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer


# FAQ Views


class FaqListCreateView(generics.ListCreateAPIView):
    queryset = Faq.objects.all()
    serializer_class = FaqSerializer


class FaqDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Faq.objects.all()
    serializer_class = FaqSerializer


# Testimonial Views


class TestimonialListCreateView(generics.ListCreateAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TestimonialSmallSerializer
        return TestimonialSerializer


class TestimonialDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer


# BlogCategory Views


class BlogCategoryListCreateView(generics.ListCreateAPIView):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer


class BlogCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    lookup_field = "slug"


# BlogTag Views


class BlogTagListCreateView(generics.ListCreateAPIView):
    queryset = BlogTag.objects.all()
    serializer_class = BlogTagSerializer


class BlogTagDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogTag.objects.all()
    serializer_class = BlogTagSerializer


# OurPartner Views


class OurPartnerListCreateView(generics.ListCreateAPIView):
    queryset = OurPartner.objects.all()
    serializer_class = OurPartnerSerializer


class OurPartnerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OurPartner.objects.all()
    serializer_class = OurPartnerSerializer


# Gallery Views


class GalleryListCreateView(generics.ListCreateAPIView):
    queryset = Gallery.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GallerySmallSerializer
        return GallerySerializer

    def get_queryset(self):
        queryset = Gallery.objects.all()
        media_type = self.request.query_params.get("media_type", None)
        if media_type:
            queryset = queryset.filter(media_type=media_type)
        return queryset


class GalleryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer


class LeaveFormListCreateView(generics.ListCreateAPIView):
    serializer_class = LeaveFormSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = LeaveForm.objects.all().order_by("-created_at")
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")
        search = self.request.query_params.get("search")
        if start_date and end_date:
            queryset = queryset.filter(leave_from_date__range=[start_date, end_date])
        elif start_date:
            queryset = queryset.filter(leave_from_date=start_date)
        if search:
            queryset = queryset.filter(employee_name__icontains=search)
        return queryset


class LeaveFormDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LeaveForm.objects.all()
    serializer_class = LeaveFormSerializer


class TestResendView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Send email using Resend
            params = {
                "from": "BaliyoVenturesContactForm <contact@baliyoventures.com>",
                "to": "ratish.shakya149@gmail.com",
                "subject": "Test Email from BaliyoVentures",
                "html": "This is a test email sent using Resend.",
            }

            resend.Emails.send(params)
            return Response(
                {"detail": "Email sent successfully"}, status=status.HTTP_200_OK
            )

        except Exception as e:
            # Log the error and still return success to the user
            print(f"Error sending email via Resend: {str(e)}")
            return Response(
                {"detail": "Failed to send email"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
