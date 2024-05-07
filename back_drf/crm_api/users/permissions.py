from rest_framework.permissions import BasePermission


# The group of the roles in system
class BaseRole(BasePermission):
    role = ""
    role_2 = ""

    def has_permission(self, request, view):
        user = request.user
        return getattr(user, self.role or self.role_2, False)


class Administrator(BaseRole):
    role = "is_superuser"


class Manager(BaseRole):
    role = "is_manager"


class Client(BaseRole):
    role = "is_client"


class AdministratorOrManager(BaseRole):
    role = "is_superuser"
    role_2 = "is_manager"
