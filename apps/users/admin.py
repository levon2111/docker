from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.models import User, CompanyAdmins


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = [
        'role',
        'username',
        'first_name',
        'last_name',
        'address',
        'email',
    ]

    def get_fieldsets(self, request, obj=None):
        add_fieldsets = (
            (None, {
                'classes': ('wide',),
                'fields': ('username', 'email', 'first_name', 'last_name', 'address', 'password1', 'password2'),
            }),
        )
        if not obj:
            return add_fieldsets
        return super().get_fieldsets(request, obj)


@admin.register(CompanyAdmins)
class CompanyAdminsAdmin(admin.ModelAdmin):
    def user(self, obj):
        return '%s %s' % (obj.user.first_name, obj.user.last_name)

    def company(self, obj):
        return '%s' % obj.company.name

    list_display = [
        'user',
        'company',
    ]
