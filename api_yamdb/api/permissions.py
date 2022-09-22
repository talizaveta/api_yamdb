from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Пользователь является администратором при редактировании."""

    def has_permission(self, request, view):
        return (request.methods in permissions.SAFE_METHODS
                or request.user.is_admin or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return (request.methods in permissions.SAFE_METHODS
                or request.user.is_admin or request.user.is_superuser)
