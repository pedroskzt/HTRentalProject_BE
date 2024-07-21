from rest_framework import permissions


class IsManager(permissions.BasePermission):
    """
    Allows access only to manager users.
    """

    def has_permission(self, request, view):
        return request.user.groups.all().filter(name="Manager").exists()


class IsAdminOrManager(permissions.BasePermission):
    """
    Allows access only to admin or Manager users.
    """

    def has_permission(self, request, view):
        user = request.user
        return user.groups.all().filter(name="Manager").exists() or user.is_superuser
