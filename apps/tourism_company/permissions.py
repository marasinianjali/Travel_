from rest_framework import permissions

from rest_framework.permissions import BasePermission
from rest_framework_api_key.permissions import HasAPIKey
# only if you're in a different file


class IsAdminOrTourismCompanyOrAPIKey(BasePermission):
    """
    Allow access if the request has a valid API key,
    OR the user is an admin or in the TourismCompany group.
    """
    def has_permission(self, request, view):
        # Allow if valid API key
        if HasAPIKey().has_permission(request, view):
            return True

        # Allow if user is authenticated and is admin or tourism company
        return IsAdminOrTourismCompany().has_permission(request, view)

class IsAdmin(permissions.BasePermission):
    """
    Custom permission to allow only Admin group members or superusers.
    """
    def has_permission(self, request, view):
        return (
            request.user
            and (request.user.is_superuser or request.user.groups.filter(name='Admin').exists())
        )

class IsTourismCompany(permissions.BasePermission):
    """
    Custom permission to only allow tourism companies to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='TourismCompany').exists()
    
class IsUser(permissions.BasePermission):
    """
    Custom permission to only allow users to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='User').exists()    
    
    
class IsAdminOrTourismCompany(permissions.BasePermission):
    """
    Allow access to users in Admin or TourismCompany group or superusers.
    """
    def has_permission(self, request, view):
        return (
            request.user and (
                request.user.is_superuser or
                request.user.groups.filter(name='Admin').exists() or
                request.user.groups.filter(name='TourismCompany').exists()
            )
        )
