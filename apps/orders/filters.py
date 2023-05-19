from django_filters import CharFilter, FilterSet

from apps.orders.models import Orders


class OrderFilter(FilterSet):
    user_id = CharFilter(field_name="user_id")

    class Meta:
        model = Orders
        fields = ["user_id"]
