from rest_framework.permissions import BasePermission


class IsAuthor(BasePermission):
    """Проверка, является ли пользователь автором привычки."""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
