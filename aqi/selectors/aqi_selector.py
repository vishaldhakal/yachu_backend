from typing import Optional

from django.db.models import QuerySet

from ..models import AQI


def get_all_aqi() -> QuerySet[AQI]:
    """
    Returns an optimized queryset of all AQI records ordered by dateTime descending.
    """
    return AQI.objects.only("id", "aqi", "dateTime").order_by("-dateTime")


def get_latest_aqi() -> Optional[AQI]:
    """
    Returns the most recent AQI record, or None if no records exist.
    """
    return AQI.objects.only("id", "aqi", "dateTime").order_by("-dateTime").first()
