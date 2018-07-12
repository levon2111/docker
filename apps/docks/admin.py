from django.contrib import admin

from apps.docks.models import Company, Warehouse


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'image',
    ]


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    def company(self, obj):
        return obj.company.name

    list_display = [
        'name',
        'company',
        'open_date',
        'close_date',
        'opened_overnight',
    ]
