from rest_framework import serializers

from .models import (
    BillOfMaterial,
    Blog,
    BlogCategory,
    BlogTag,
    Component,
    ComponentModel,
    ComponentPurchase,
    ComponentPurchaseItem,
    Contact,
    Faq,
    Gallery,
    Image,
    Inventory,
    LeaveForm,
    OurPartner,
    Project,
    ProjectDailyUpdate,
    ProjectDemo,
    ProjectInventoryUsed,
    ProjectTool,
    Service,
    TeamMember,
    TechnicalDocument,
    Testimonial,
    Vendor,
)


class ProjectSmallSerializer(serializers.ModelSerializer):
    thumbnail_image = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "slug",
            "status",
            "thumbnail_image",
            "thumbnail_image_alt_description",
            "meta_description",
            "meta_title",
        ]

    def get_thumbnail_image(self, obj):
        request = self.context.get("request")

        if obj.thumbnail_image:
            if request:
                return request.build_absolute_uri(obj.thumbnail_image.url)
            return obj.thumbnail_image.url

        return None


class ServiceSerializer(serializers.ModelSerializer):
    projects = serializers.SerializerMethodField()

    class Meta:
        model = Service
        exclude = ["created_at", "updated_at"]

    def get_projects(self, obj):
        projects = obj.projects.filter(status="completed").order_by("-created_at")

        return ProjectSmallSerializer(projects, many=True, context=self.context).data


class ServiceSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = [
            "id",
            "title",
            "slug",
            "icon",
            "thumbnail_image",
            "thumbnail_image_alt_description",
            "short_description",
        ]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class ProjectDemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDemo
        fields = "__all__"


class TechnicalDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalDocument
        fields = "__all__"


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = "__all__"


class ProjectToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTool
        fields = "__all__"


class ComponentModelSerializer(serializers.ModelSerializer):
    component_name = serializers.CharField(source="component.name", read_only=True)

    class Meta:
        model = ComponentModel
        fields = "__all__"


class ComponentSmallSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(
        source="vendor.name", read_only=True, default=None
    )
    no_of_models = serializers.IntegerField(source="models.count", read_only=True)
    models_count = serializers.IntegerField(source="models.count", read_only=True)

    class Meta:
        model = Component
        fields = [
            "id",
            "name",
            "slug",
            "vendor",
            "vendor_name",
            "no_of_models",
            "models_count",
            "created_at",
            "updated_at",
        ]


class ComponentSerializer(serializers.ModelSerializer):
    vendor_details = VendorSerializer(source="vendor", read_only=True)
    vendor_name = serializers.CharField(
        source="vendor.name", read_only=True, default=None
    )
    no_of_models = serializers.IntegerField(source="models.count", read_only=True)
    models_count = serializers.IntegerField(source="models.count", read_only=True)
    models = serializers.SerializerMethodField()

    class Meta:
        model = Component
        fields = "__all__"

    def get_models(self, obj):
        if not hasattr(obj, "models"):
            return []
        models = obj.models.all().order_by("-created_at")
        return ComponentModelSerializer(models, many=True, context=self.context).data


class InventorySerializer(serializers.ModelSerializer):
    model_name = serializers.CharField(
        source="component_model.name", read_only=True, default=None
    )
    component_name = serializers.CharField(
        source="component_model.component.name", read_only=True, default=None
    )
    vendor_name = serializers.CharField(
        source="component_model.component.vendor.name", read_only=True, default=None
    )
    component_model_details = ComponentModelSerializer(
        source="component_model", read_only=True
    )

    class Meta:
        model = Inventory
        fields = "__all__"


class ProjectInventoryUsedSerializer(serializers.ModelSerializer):
    inventory_details = InventorySerializer(source="inventory", read_only=True)
    project_title = serializers.CharField(source="project.title", read_only=True)

    class Meta:
        model = ProjectInventoryUsed
        fields = "__all__"


class ProjectDailyUpdateSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source="project.title", read_only=True)
    project_slug = serializers.CharField(source="project.slug", read_only=True)

    class Meta:
        model = ProjectDailyUpdate
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    category = ServiceSmallSerializer(many=True, read_only=True)
    demos = ProjectDemoSerializer(many=True, read_only=True)
    technical_document = TechnicalDocumentSerializer(many=True, read_only=True)
    technical_documents = TechnicalDocumentSerializer(
        source="technical_document", many=True, read_only=True
    )
    components_used = ProjectInventoryUsedSerializer(many=True, read_only=True)
    daily_updates = serializers.SerializerMethodField()
    tools = ProjectToolSerializer(many=True, read_only=True)
    tool_ids = serializers.PrimaryKeyRelatedField(
        queryset=ProjectTool.objects.all(),
        write_only=True,
        many=True,
        required=False,
    )
    # Accepts a list of tool names — creates the tool if it doesn't exist
    tool_names = serializers.ListField(
        child=serializers.CharField(max_length=255),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Project
        fields = "__all__"

    def get_daily_updates(self, obj):
        updates = obj.daily_updates.all().order_by("-created_at")
        return ProjectDailyUpdateSerializer(
            updates, many=True, context=self.context
        ).data

    def create(self, validated_data):
        tool_ids = validated_data.pop("tool_ids", None)
        tool_names = validated_data.pop("tool_names", None)

        instance = super().create(validated_data)

        if tool_ids is not None:
            instance.tools.set(tool_ids)

        if tool_names is not None:
            current_ids = set(instance.tools.values_list("id", flat=True))
            for name in tool_names:
                tool, _ = ProjectTool.objects.get_or_create(
                    name__iexact=name.strip(),
                    defaults={"name": name.strip()},
                )
                current_ids.add(tool.id)
            instance.tools.set(current_ids)

        return instance

    def update(self, instance, validated_data):
        tool_ids = validated_data.pop("tool_ids", None)
        tool_names = validated_data.pop("tool_names", None)

        instance = super().update(instance, validated_data)

        # If tool_ids provided, set directly
        if tool_ids is not None:
            instance.tools.set(tool_ids)

        # If tool_names provided, get_or_create each and append to existing tools
        if tool_names is not None:
            current_ids = set(instance.tools.values_list("id", flat=True))
            for name in tool_names:
                tool, _ = ProjectTool.objects.get_or_create(
                    name__iexact=name.strip(),
                    defaults={"name": name.strip()},
                )
                current_ids.add(tool.id)
            instance.tools.set(current_ids)

        return instance


class BlogTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = "__all__"


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = "__all__"


class BlogSerializer(serializers.ModelSerializer):
    category = BlogCategorySerializer(read_only=True)
    tags = BlogTagSerializer(many=True, read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=BlogCategory.objects.all(), source="category", write_only=True
    )
    tag_id = serializers.PrimaryKeyRelatedField(
        queryset=BlogTag.objects.all(),
        source="tags",
        write_only=True,
        many=True,
        required=False,
    )

    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "thumbnail_image",
            "thumbnail_image_alt_description",
            "category",
            "category_id",
            "tags",
            "tag_id",
            "created_at",
            "updated_at",
        ]


class BlogSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "slug",
            "thumbnail_image",
            "thumbnail_image_alt_description",
            "meta_title",
            "meta_description",
        ]


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = "__all__"


class TeamMemberSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = "__all__"


class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = "__all__"


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = "__all__"


class TestimonialSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = [
            "id",
            "name",
            "message",
            "rating",
            "designation",
            "image",
            "image_alt_description",
        ]


class OurPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OurPartner
        fields = "__all__"


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = "__all__"


class GallerySmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ["id", "title", "media", "media_type", "media_alt_description"]


class LeaveFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveForm
        fields = "__all__"


class BillOfMaterialSerializer(serializers.ModelSerializer):
    vendor_details = VendorSerializer(source="vendor", read_only=True)

    class Meta:
        model = BillOfMaterial
        fields = "__all__"


class ComponentPurchaseItemSerializer(serializers.ModelSerializer):
    component_model_name = serializers.CharField(
        source="component_model.name", read_only=True, default=None
    )
    component_name = serializers.CharField(
        source="component_model.component.name", read_only=True, default=None
    )
    component_slug = serializers.CharField(
        source="component_model.component.slug", read_only=True, default=None
    )
    component_model_slug = serializers.CharField(
        source="component_model.slug", read_only=True, default=None
    )

    class Meta:
        model = ComponentPurchaseItem
        fields = [
            "id",
            "component_model",
            "component_model_name",
            "component_name",
            "component_slug",
            "component_model_slug",
            "quantity",
            "price_per_item",
            "total_price",
            "created_at",
        ]


class ComponentPurchaseListSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(
        source="vendor.name", read_only=True, default=None
    )
    vendor_phone = serializers.CharField(
        source="vendor.phone_no", read_only=True, default=None
    )
    vendor_address = serializers.CharField(
        source="vendor.vendor_address", read_only=True, default=None
    )

    class Meta:
        model = ComponentPurchase
        fields = [
            "id",
            "vendor",
            "vendor_name",
            "vendor_phone",
            "vendor_address",
            "purchase_date",
            "total_price",
            "notes",
            "created_at",
            "updated_at",
        ]


class ComponentPurchaseDetailSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(
        source="vendor.name", read_only=True, default=None
    )
    vendor_phone = serializers.CharField(
        source="vendor.phone_no", read_only=True, default=None
    )
    vendor_address = serializers.CharField(
        source="vendor.vendor_address", read_only=True, default=None
    )
    items = ComponentPurchaseItemSerializer(many=True, read_only=True)

    class Meta:
        model = ComponentPurchase
        fields = [
            "id",
            "vendor",
            "vendor_name",
            "vendor_phone",
            "vendor_address",
            "purchase_date",
            "total_price",
            "notes",
            "items",
            "created_at",
            "updated_at",
        ]


# Alias for backward compatibility if imported elsewhere
ComponentPurchaseSerializer = ComponentPurchaseDetailSerializer
