from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """
    Проверка на модератора
    """

    message = "Только модераторы могут просматривать данный объект."

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderator").exists()
