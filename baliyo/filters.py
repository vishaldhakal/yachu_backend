import django_filters

from .models import Component, ComponentModel, Inventory, ProjectTool, Vendor


class VendorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    phone_no = django_filters.CharFilter(field_name="phone_no", lookup_expr="icontains")

    class Meta:
        model = Vendor
        fields = ["name", "phone_no"]


class ProjectToolFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = ProjectTool
        fields = ["name"]


class ComponentFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    vendor = django_filters.NumberFilter(field_name="vendor__id", lookup_expr="exact")
    vendor_name = django_filters.CharFilter(
        field_name="vendor__name", lookup_expr="icontains"
    )

    class Meta:
        model = Component
        fields = ["name", "vendor", "vendor_name"]


class ComponentModelFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    component = django_filters.NumberFilter(
        field_name="component__id", lookup_expr="exact"
    )
    component_name = django_filters.CharFilter(
        field_name="component__name", lookup_expr="icontains"
    )

    class Meta:
        model = ComponentModel
        fields = ["name", "component", "component_name"]


class InventoryFilter(django_filters.FilterSet):
    component_model = django_filters.NumberFilter(
        field_name="component_model__id", lookup_expr="exact"
    )
    component_model_name = django_filters.CharFilter(
        field_name="component_model__name", lookup_expr="icontains"
    )
    component = django_filters.NumberFilter(
        field_name="component_model__component__id", lookup_expr="exact"
    )
    component_name = django_filters.CharFilter(
        field_name="component_model__component__name", lookup_expr="icontains"
    )
    vendor = django_filters.NumberFilter(
        field_name="component_model__component__vendor__id", lookup_expr="exact"
    )
    vendor_name = django_filters.CharFilter(
        field_name="component_model__component__vendor__name", lookup_expr="icontains"
    )
    min_quantity = django_filters.NumberFilter(field_name="quantity", lookup_expr="gte")
    max_quantity = django_filters.NumberFilter(field_name="quantity", lookup_expr="lte")

    class Meta:
        model = Inventory
        fields = [
            "component_model",
            "component_model_name",
            "component",
            "component_name",
            "vendor",
            "vendor_name",
            "min_quantity",
            "max_quantity",
        ]
