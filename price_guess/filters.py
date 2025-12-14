import django_filters

from .models import PriceGuess


class PriceGuessFilter(django_filters.FilterSet):
    # Yachu Facewash Price Filters
    yachu_facewash_price = django_filters.NumberFilter(
        field_name="yachu_facewash_price", lookup_expr="exact"
    )
    # Yachu Body Lotion Price Filters
    yachu_bodylotion_price = django_filters.NumberFilter(
        field_name="yachu_bodylotion_price", lookup_expr="exact"
    )
    # Yachu Brightening Cream Price Filters
    yachu_brightening_cream_price = django_filters.NumberFilter(
        field_name="yachu_brightening_cream_price", lookup_expr="exact"
    )

    class Meta:
        model = PriceGuess
        fields = [
            "yachu_facewash_price",
            "yachu_bodylotion_price",
            "yachu_brightening_cream_price",
        ]
