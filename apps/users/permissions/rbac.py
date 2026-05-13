from rest_framework.permissions import BasePermission
from apps.users.services.permission_service import has_permission


class HasRBACPermission(BasePermission):
    
    def has_permission(self, request, view):
        
        required_permission = getattr(
            view,
            'required_permission',
            None
        )
        
        if not required_permission:
            return False
        
        return has_permission(request.user, required_permission)