import django_filters
import rest_framework_filters as filters

from apps.core.filters import BaseFilter
from apps.users.models import CompanyWarehouseAdmins


class WarehouseAdminFilter(filters.FilterSet, BaseFilter):
    user_email = django_filters.CharFilter(method='filter_by_company')
    user_first_name = django_filters.CharFilter(method='filter_by_company')
    user_last_name = django_filters.CharFilter(method='filter_by_company')
    user_address = django_filters.CharFilter(method='filter_by_company')

    def filter_by_company(self, queryset, name, value):
        return queryset.filter(company__id=value)

    class Meta:
        model = CompanyWarehouseAdmins
        fields = {}
