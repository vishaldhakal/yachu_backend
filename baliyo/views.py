import os

import resend
from django.db.models import Q
from django.template.loader import render_to_string
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

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
    Service,
    TeamMember,
    TechnicalDocument,
    Testimonial,
)
from .selectors import (
    component_list_select,
    component_model_list_select,
    component_purchase_list_select,
    inventory_list_select,
    project_daily_update_list_select,
    project_inventory_used_list_select,
    project_tool_list_select,
    vendor_list_select,
)
from .serializers import (
    BlogCategorySerializer,
    BlogSerializer,
    BlogSmallSerializer,
    BlogTagSerializer,
    ComponentModelSerializer,
    ComponentPurchaseDetailSerializer,
    ComponentPurchaseListSerializer,
    ComponentSerializer,
    ComponentSmallSerializer,
    ContactSerializer,
    FaqSerializer,
    GallerySerializer,
    GallerySmallSerializer,
    ImageSerializer,
    InventorySerializer,
    LeaveFormSerializer,
    OurPartnerSerializer,
    ProjectDailyUpdateSerializer,
    ProjectDemoSerializer,
    ProjectInventoryUsedSerializer,
    ProjectSerializer,
    ProjectSmallSerializer,
    ProjectToolSerializer,
    ServiceSerializer,
    ServiceSmallSerializer,
    TeamMemberSerializer,
    TeamMemberSmallSerializer,
    TechnicalDocumentSerializer,
    TestimonialSerializer,
    TestimonialSmallSerializer,
    VendorSerializer,
)
from .services import (
    component_create,
    component_model_create,
    component_purchase_create,
    component_purchase_update,
    project_daily_update_create,
    project_inventory_used_create,
    project_tool_create,
    vendor_create,
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
        search = self.request.query_params.get("search", None)
        status_param = self.request.query_params.get("status", None)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        if status_param:
            queryset = queryset.filter(status=status_param)
        if search:
            queryset = queryset.filter(Q(title__icontains=search)).distinct()
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProjectSmallSerializer
        return ProjectSerializer

    def perform_create(self, serializer):
        project = serializer.save()
        category_param = self.request.query_params.get(
            "category", "product-development"
        )
        service = Service.objects.filter(slug=category_param).first()
        if not service:
            service = Service.objects.filter(slug="product-development").first()
        if not service:
            service = Service.objects.filter(title__icontains="product").first()
        if service:
            project.category.add(service)


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all().prefetch_related(
        "images", "category", "demos", "technical_document"
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
            .distinct()[:4]
        )

        response_data = serializer.data
        response_data["similar_projects"] = ProjectSmallSerializer(
            similar_projects, many=True, context={"request": request}
        ).data

        return Response(response_data)


# ProjectDemo Views


class ProjectDemoListCreateView(generics.ListCreateAPIView):
    queryset = ProjectDemo.objects.all().select_related("project")
    serializer_class = ProjectDemoSerializer


class ProjectDemoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProjectDemo.objects.all().select_related("project")
    serializer_class = ProjectDemoSerializer


# TechnicalDocument Views


class TechnicalDocumentListCreateView(generics.ListCreateAPIView):
    queryset = TechnicalDocument.objects.all().select_related("project")
    serializer_class = TechnicalDocumentSerializer


class TechnicalDocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TechnicalDocument.objects.all().select_related("project")
    serializer_class = TechnicalDocumentSerializer


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


# Vendor Views


class VendorListCreateView(generics.ListCreateAPIView):
    serializer_class = VendorSerializer

    def get_queryset(self):
        return vendor_list_select()

    def perform_create(self, serializer):
        serializer.instance = vendor_create(
            name=serializer.validated_data.get("name"),
            phone_no=serializer.validated_data.get("phone_no"),
            vendor_address=serializer.validated_data.get("vendor_address"),
        )


class VendorDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VendorSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return vendor_list_select()


# ProjectTool Views


class ProjectToolListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectToolSerializer

    def get_queryset(self):
        return project_tool_list_select()

    def perform_create(self, serializer):
        serializer.instance = project_tool_create(
            name=serializer.validated_data.get("name")
        )


class ProjectToolDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectToolSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return project_tool_list_select()


# Component Views


class ComponentListCreateView(generics.ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == "GET":
            return ComponentSmallSerializer
        return ComponentSerializer

    def get_queryset(self):
        return component_list_select()

    def perform_create(self, serializer):
        serializer.instance = component_create(
            name=serializer.validated_data.get("name"),
            vendor=serializer.validated_data.get("vendor"),
        )


class ComponentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ComponentSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return component_list_select()


# ComponentModel Views


class ComponentModelListCreateView(generics.ListCreateAPIView):
    serializer_class = ComponentModelSerializer

    def get_queryset(self):
        queryset = component_model_list_select()
        search = self.request.query_params.get("search", None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(component__name__icontains=search)
            ).distinct()
        return queryset

    def perform_create(self, serializer):
        serializer.instance = component_model_create(
            component=serializer.validated_data.get("component"),
            name=serializer.validated_data.get("name"),
            specs=serializer.validated_data.get("specs"),
        )


class ComponentModelDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ComponentModelSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return component_model_list_select()


# ComponentPurchase Views


class ComponentPurchaseListCreateView(generics.ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == "POST":
            return ComponentPurchaseDetailSerializer
        return ComponentPurchaseListSerializer

    def get_queryset(self):
        return component_purchase_list_select()

    def perform_create(self, serializer):
        items_data = self.request.data.get("items", [])
        serializer.instance = component_purchase_create(
            vendor=serializer.validated_data.get("vendor"),
            purchase_date=serializer.validated_data.get("purchase_date"),
            notes=serializer.validated_data.get("notes"),
            component_model=None,
            quantity=0,
            price_per_item=0.0,
            items_data=items_data,
        )


class ComponentPurchaseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ComponentPurchaseDetailSerializer

    def get_queryset(self):
        return component_purchase_list_select()

    def perform_update(self, serializer):
        items_data = self.request.data.get("items", None)
        serializer.instance = component_purchase_update(
            purchase=self.get_object(),
            vendor=serializer.validated_data.get("vendor", serializer.instance.vendor),
            purchase_date=serializer.validated_data.get(
                "purchase_date", serializer.instance.purchase_date
            ),
            notes=serializer.validated_data.get("notes", serializer.instance.notes),
            items_data=items_data
            if items_data is not None
            else [
                {
                    "component_model": item.component_model_id,
                    "quantity": item.quantity,
                    "price_per_item": item.price_per_item,
                }
                for item in serializer.instance.items.all()
            ],
        )


# Inventory Views


class InventoryListCreateView(generics.ListCreateAPIView):
    serializer_class = InventorySerializer

    def get_queryset(self):
        return inventory_list_select()


class InventoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InventorySerializer

    def get_queryset(self):
        return inventory_list_select()


# ProjectInventoryUsed Views


class ProjectInventoryUsedListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectInventoryUsedSerializer

    def get_queryset(self):
        queryset = project_inventory_used_list_select()
        project_id = self.request.query_params.get("project", None)
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            instance = project_inventory_used_create(
                project_id=serializer.validated_data.get("project").id,
                inventory=serializer.validated_data.get("inventory"),
                quantity=serializer.validated_data.get("quantity", 0),
            )
            return Response(
                ProjectInventoryUsedSerializer(
                    instance, context={"request": request}
                ).data,
                status=status.HTTP_201_CREATED,
            )
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProjectInventoryUsedDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectInventoryUsedSerializer

    def get_queryset(self):
        return project_inventory_used_list_select()


# ProjectDailyUpdate Views


class ProjectDailyUpdateListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectDailyUpdateSerializer

    def get_queryset(self):
        queryset = project_daily_update_list_select()
        project_id = self.request.query_params.get("project", None)
        category_slug = self.request.query_params.get("category", None)
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        if category_slug:
            queryset = queryset.filter(project__category__slug=category_slug)
        return queryset.distinct()

    def perform_create(self, serializer):
        serializer.instance = project_daily_update_create(
            project_id=serializer.validated_data.get("project").id,
            task=serializer.validated_data.get("task"),
            decision=serializer.validated_data.get("decision"),
            reason=serializer.validated_data.get("reason"),
            problem=serializer.validated_data.get("problem"),
        )


class ProjectDailyUpdateDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectDailyUpdateSerializer

    def get_queryset(self):
        return project_daily_update_list_select()
