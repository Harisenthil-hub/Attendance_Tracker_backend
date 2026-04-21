from uuid6 import uuid7
from django.db import models
from django.db.models import Q
from .user import User


class Role(models.Model):
    
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid7, unique=True, editable=False)
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    
    
class UserRole(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_users')
    
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='assigned_roles')
    removed_by = models.ForeignKey(User, on_delete=models.SET_NULL,  blank=True, null=True, related_name='removed_roles')
    
    assigned_at = models.DateTimeField(auto_now_add=True)
    removed_at = models.DateTimeField(null=True, blank=True)
    
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'role'],
                condition=Q(removed_at__isnull=True),
                name='unique_active_user_role'
            )
        ]
        
        
    def __str__(self):
        return f"{self.user.email} -> {self.role.name}"
    
    
    
    
