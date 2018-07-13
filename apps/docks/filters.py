import django_filters
import rest_framework_filters as filters

from apps.core.filters import BaseFilter
from apps.docks.models import Warehouse


class WarehouseFilter(filters.FilterSet, BaseFilter):
    company = django_filters.CharFilter(method='filter_by_company')

    def filter_by_company(self, queryset, name, value):
        return queryset.filter(company__id=value)

    class Meta:
        model = Warehouse
        fields = {
            'name': ['icontains', ],
            'opened_overnight': ['exact', ],
        }
