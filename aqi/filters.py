import django_filters

from .models import AQI


class AQIFilter(django_filters.FilterSet):
    """
    FilterSet for AQI records supporting date range and value filtering.
    """

    start_date = django_filters.DateFilter(
        field_name="dateTime__date", lookup_expr="gte"
    )
    end_date = django_filters.DateFilter(field_name="dateTime__date", lookup_expr="lte")
    aqi = django_filters.CharFilter(field_name="aqi", lookup_expr="icontains")

    class Meta:
        model = AQI
        fields = ["aqi", "start_date", "end_date"]
