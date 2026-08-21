from django.db.models import (
    ExpressionWrapper,
    F,
    FloatField,
    OuterRef,
    QuerySet,
    Subquery,
)
from django.db.models.functions import Coalesce

from ..models import (
    BillOfMaterial,
    Component,
    ComponentModel,
    ComponentPurchase,
    ComponentPurchaseItem,
    Inventory,
    ProjectDailyUpdate,
    ProjectInventoryUsed,
    ProjectTool,
    ProjectToolUsed,
    Vendor,
)


def vendor_list_select() -> QuerySet[Vendor]:
    return Vendor.objects.all().order_by("-created_at")


def vendor_detail_select(vendor_id: int) -> Vendor:
    return Vendor.objects.filter(id=vendor_id).first()


def vendor_detail_select_by_slug(slug: str) -> Vendor:
    return Vendor.objects.filter(slug=slug).first()


def bill_of_material_list_select() -> QuerySet[BillOfMaterial]:
    return BillOfMaterial.objects.all().select_related("vendor").order_by("-created_at")


def project_tool_list_select() -> QuerySet[ProjectTool]:
    return ProjectTool.objects.all().order_by("-created_at")


def project_tool_used_list_select() -> QuerySet[ProjectToolUsed]:
    return (
        ProjectToolUsed.objects
        .all()
        .select_related("project", "tool")
        .order_by("-created_at")
    )

def project_tool_detail_select_by_slug(slug: str) -> ProjectTool:
    return ProjectTool.objects.filter(slug=slug).first()


def component_list_select() -> QuerySet[Component]:
    return Component.objects.all().select_related("vendor").order_by("-created_at")


def component_detail_select(component_id: int) -> Component:
    return (
        Component.objects
        .filter(id=component_id)
        .select_related("vendor")
        .prefetch_related("models")
        .first()
    )


def component_detail_select_by_slug(slug: str) -> Component:
    return (
        Component.objects
        .filter(slug=slug)
        .select_related("vendor")
        .prefetch_related("models")
        .first()
    )


def component_model_detail_select_by_slug(slug: str) -> ComponentModel:
    return (
        ComponentModel.objects
        .filter(slug=slug)
        .select_related("component", "component__vendor")
        .first()
    )


def component_model_list_select() -> QuerySet[ComponentModel]:
    return (
        ComponentModel.objects
        .all()
        .select_related("component", "component__vendor")
        .order_by("-created_at")
    )


def component_purchase_list_select() -> QuerySet[ComponentPurchase]:
    return (
        ComponentPurchase.objects
        .all()
        .select_related(
            "vendor",
            "project",
        )
        .prefetch_related(
            "items",
            "items__component_model",
            "items__component_model__component",
            "items__component_model__component__vendor",
        )
        .order_by("-created_at")
    )


def inventory_list_select() -> QuerySet[Inventory]:
    latest_unit_price = Subquery(
        ComponentPurchaseItem.objects.filter(
            component_model=OuterRef("component_model")
        )
        .order_by("-created_at")
        .values("price_per_item")[:1],
        output_field=FloatField(),
    )

    return (
        Inventory.objects
        .all()
        .select_related(
            "component_model",
            "component_model__component",
            "component_model__component__vendor",
        )
        .annotate(
            _unit_price=Coalesce(latest_unit_price, 0.0, output_field=FloatField())
        )
        .annotate(
            _total_price=ExpressionWrapper(
                F("quantity") * F("_unit_price"),
                output_field=FloatField(),
            )
        )
        .order_by("-created_at")
    )


def project_inventory_used_list_select() -> QuerySet[ProjectInventoryUsed]:
    return (
        ProjectInventoryUsed.objects
        .all()
        .select_related(
            "project",
            "inventory",
            "inventory__component_model",
            "inventory__component_model__component",
            "inventory__component_model__component__vendor",
        )
        .order_by("-created_at")
    )


def project_daily_update_list_select() -> QuerySet[ProjectDailyUpdate]:
    return (
        ProjectDailyUpdate.objects
        .all()
        .select_related("project")
        .order_by("-created_at")
    )
