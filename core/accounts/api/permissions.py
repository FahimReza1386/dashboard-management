# Third-Party Imports
from rest_framework.permissions import BasePermission

# Locale Imports
from accounts.models import Users


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.type == Users.UserTypeModel.superuser.value
                    and request.user.is_superuser)
