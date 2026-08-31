from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение на редактирование только владельцем объекта.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешаем безопасные методы всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # Проверяем, что пользователь является владельцем
        return obj.user == request.user


class IsOwnerOrStaff(permissions.BasePermission):
    """
    Разрешение для владельца или персонала.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff
