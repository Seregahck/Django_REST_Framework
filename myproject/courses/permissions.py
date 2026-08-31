from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """
    Разрешение для модераторов на просмотр и изменение, но не создание и удаление.
    """

    def has_permission(self, request, view):
        # Проверяем, что пользователь аутентифицирован
        if not request.user or not request.user.is_authenticated:
            return False

        # Проверяем, состоит ли пользователь в группе модераторов
        return request.user.groups.filter(name='moderators').exists()


class IsModeratorOrOwner(permissions.BasePermission):
    """
    Разрешение для модераторов на просмотр и изменение всех объектов,
    а для обычных пользователей только на свои объекты.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # Для безопасных методов разрешаем всем аутентифицированным
        if request.method in permissions.SAFE_METHODS:
            return True

        # Для создания объектов проверяем, что пользователь не модератор
        if request.method == 'POST':
            return not request.user.groups.filter(name='moderators').exists()

        return True

    def has_object_permission(self, request, view, obj):
        # Модератор может просматривать и изменять любые объекты
        if request.user.groups.filter(name='moderators').exists():
            # Но модератор не может удалять
            if request.method == 'DELETE':
                return False
            return True

        # Обычный пользователь может работать только со своими объектами
        return obj.owner == request.user


class IsOwner(permissions.BasePermission):
    """
    Разрешение только для владельца объекта.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
