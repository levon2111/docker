import django_filters
import rest_framework_filters as filters

from apps.core.filters import BaseFilter
from apps.docks.models import Warehouse, BookedDock


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


class BookedDockFilter(filters.FilterSet, BaseFilter):
    warehouse = django_filters.CharFilter(method='filter_by_warehouse')
    start_date = django_filters.CharFilter(method='filter_by_startdate')
    end_date = django_filters.CharFilter(method='filter_by_enddate')

    def filter_by_startdate(self, queryset, name, value):
        return queryset.filter(start_date__lte=value, end_date__gte=value)

    def filter_by_enddate(self, queryset, name, value):
        return queryset.filter(start_date__lte=value, end_date__gte=value)

    def filter_by_warehouse(self, queryset, name, value):
        return queryset.filter(dock__warehouse=value)

    class Meta:
        model = BookedDock
        fields = {

        }
