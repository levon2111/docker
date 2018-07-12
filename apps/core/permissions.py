from rest_framework import permissions


class BasePermission(permissions.BasePermission):
    pass


class IsAdminOrSafeMethod(BasePermission):
    """
    Permission check for admin or access for safe methods
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated() and request.user.role == 'admin'


class IsAdmin(BasePermission):
    """
    Permission check for admin
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated() and request.user.role == 'admin'
