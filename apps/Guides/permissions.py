from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and (request.user.is_superuser or request.user.groups.filter(name='Admin').exists())
        )

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Manager').exists()

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Customer').exists()

class IsAdminOrManager(permissions.BasePermission):
    def has_permission(self, request, view):
         return (
            request.user and (
                request.user.is_superuser or
                request.user.groups.filter(name='Admin').exists() or
                request.user.groups.filter(name='TourismCompany').exists()
            )
        )