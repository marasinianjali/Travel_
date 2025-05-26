from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Custom permission to allow only Admin group members or superusers.
    """
    def has_permission(self, request, view):
        return (
            request.user
            and (request.user.is_superuser or request.user.groups.filter(name='Admin').exists())
        )

class IsHotel(permissions.BasePermission):
    """
    Custom permission to only allow hotel to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='TourismCompany').exists()
    
class IsUser(permissions.BasePermission):
    """
    Custom permission to only allow users to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='User').exists()    
    
    
class IsAdminOrHotel(permissions.BasePermission):
    """
    Allow access to users in Admin or hotel group or superusers.
    """
    def has_permission(self, request, view):
        return (
            request.user and (
                request.user.is_superuser or
                request.user.groups.filter(name='Admin').exists() or
                request.user.groups.filter(name='Hotel').exists()
            )
        )
