from apps.users.models import RolePermission

def has_permission(user, permission_name):
    
    if user.is_superuser:
        return True
    
    
    active_roles = user.user_roles.filter(
        removed_at__isnull=True
    )
    
    
    role_ids = active_roles.values_list(
        'role_id',
        flat=True
    )
    
    
    return RolePermission.objects.filter(
        role_id__in=role_ids,
        permission__name=permission_name
    ).exists()