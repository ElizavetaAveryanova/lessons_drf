from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """
    Проверка на модератора
    """

    message = "Только модераторы могут просматривать данный объект."

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderator").exists()


class IsOwner(permissions.BasePermission):
    """
    Проверка на владельца
    """

    message = "Только владельцы могут просматривать данный объект."

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        else:
            return False
