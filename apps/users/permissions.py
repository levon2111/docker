# -*- coding: utf-8 -*-

from apps.core.permissions import BasePermission


class HasUserPermissions(BasePermission):
    """
    Permission check for admin or account owner
    """

    def has_permission(self, request, view):

        if view.action in ['list', 'create', ]:
            return self._is_admin(request)

        return True

    def has_object_permission(self, request, view, obj):

        if self._is_admin(request):
            return True

        if view.action in ['retrieve', 'partial_update', ]:

            # If current model is User then check user.pk else check user.get_view_id
            if type(obj).__name__ == 'User':
                return request.user.pk == obj.pk

            return request.user.get_view_id == obj.pk

        return False
