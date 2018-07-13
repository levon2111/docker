from django.contrib import admin

from apps.docks.models import Company, Warehouse, Dock, BookedDock


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


@admin.register(Dock)
class DockAdmin(admin.ModelAdmin):
    def warehouse(self, obj):
        return obj.warehouse.name

    def company(self, obj):
        return obj.warehouse.company.name

    list_display = [
        'company',
        'warehouse',
        'name',
    ]


@admin.register(BookedDock)
class BookedDockAdmin(admin.ModelAdmin):
    def company(self, obj):
        return obj.dock.warehouse.company.name

    def dock(self, obj):
        return obj.dock.name

    def warehouse(self, obj):
        return obj.dock.warehouse.name

    list_display = [
        'company',
        'warehouse',
        'dock',
        'start_date',
        'end_date',
    ]
