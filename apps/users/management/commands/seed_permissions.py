from django.core.management.base import BaseCommand
from apps.users.models import Permission, Role, RolePermission

class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        
        permissions = [
            
            # User Management
            ('create_user', 'users'),
            ('view_user', 'users'),
            ('update_user', 'users'),
            ('delete_user', 'users'),
            
            
            
            # Teamlead Management
            ('create_teamlead', 'users'),
            
            
            # Admin Management
            ('create_admin', 'users') ,
            
            
            # Role Management
            ('assign_role', 'roles'),
            ('remove_role', 'roles'),
            
            
            # Permission Management
            ('assign_permission', 'permissions'),
        ]
        
        
        permission_map = {}
        
        for name, module in permissions:
            
            permission, _ = Permission.objects.get_or_create(
                name=name,
                defaults = {
                    'module': module
                }
            )
            
            permission_map[name] = permission
            
            
        
        # Get Roles
        
        admin_role = Role.objects.get(name='admin')
        teamlead_role = Role.objects.get(name='teamlead')
        user_role = Role.objects.get(name='user')
        
        
        # Admin Permissions
        
        for permission in permission_map.values():
            
            RolePermission.objects.get_or_create(
                role=admin_role,
                permission=permission
            )
        
        
        teamlead_permissions = []
        
        for permission_name in teamlead_permissions:
            
            RolePermission.objects.get_or_create(
                role=teamlead_role,
                permission=permission_map[name]
            )
            
        self.stdout.write(
            self.style.SUCCESS('Permissions seeded successfully')
        )