from rest_framework import serializers
from apps.users.models import User, UserProfile, UserRole, RolePermission


class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = ['full_name', 'phone', 'dob', 'gender', 'avatar_url']

class CurrentUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    roles = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    
    
    class Meta:
        model = User
        fields = ['uuid', 'username', 'email', 'status', 'is_verified', 'profile', 'created_at', 'roles', 'permissions']
        
        
    def get_roles(self, obj):
        
        active_roles = UserRole.objects.filter(
         user=obj,
         removed_at__isnull=True
        ).select_related('role')
        
        return [
            user_role.role.name 
            for user_role in active_roles
        ]
        
        
    def get_permissions(self, obj):
        role_ids = UserRole.objects.filter(
            user=obj,
            removed_at__isnull=True
        ).values_list(
            'role_id',
            flat=True
        )
        
        permissions = RolePermission.objects.filter(
            role_id__in=role_ids
        ).select_related('permission')
        
        return list(
            set(
                permission.permission.name 
                for permission in permissions
            )
        )