from rest_framework import permissions


class OnlyAuthorDeleteUpdateOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """
    Проверка авторства при обновлении/удалении либо только чтение.
    """

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user
                or request.method in permissions.SAFE_METHODS)
