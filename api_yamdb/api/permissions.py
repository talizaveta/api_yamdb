from rest_framework import permissions

from users.models import ADMIN, MODERATOR


class AdminOnly(permissions.BasePermission):
    """Пользователь является администратором или суперпользователем."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):
    """Пользователь является администратором при редактировании."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )


class ReviewAndCommentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            (request.method in permissions.SAFE_METHODS)
            or (request.user and request.user.is_authenticated)
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            return (request.user
                    and request.user.is_authenticated)
        if request.method == 'PATCH' or request.method == 'DELETE':
            return (request.user.role == ADMIN
                    or request.user.role == MODERATOR
                    or obj.author == request.user)
        return False
