from uuid6 import uuid7
from django.db import models
from .roles import Role


class Permission(models.Model):
    
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid7, unique=True, editable=False)
    
    name = models.CharField(max_length=100, unique=True)
    module = models.CharField(max_length=250, blank=True)
    
    
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    

class RolePermission(models.Model):
    
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='roles')
    
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['role', 'permission'],
                name='unique_role_permission'
            )
        ]