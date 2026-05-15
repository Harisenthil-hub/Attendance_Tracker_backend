from rest_framework import serializers
from django.db import transaction
from apps.users.models import User, UserProfile, Role, UserRole
from django.utils import timezone


class CreateUserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'role', 'joined_date']
        
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('An Account with this email already exists')
        return value
    
    
    def validate_role(self, value):
        
        if not Role.objects.filter(name=value).exists():
            raise serializers.ValidationError(f'The role {value} does not exist in the system')
        return value
    
    def validate_joined_date(self, value):
        
        if value > timezone.now().date():
            raise serializers.ValidationError('Join date cannot be in the future')
        
        return value
        
    
    def create(self, validated_data):
        
        role_name = validated_data.pop('role')
        
        
        with transaction.atomic():
        
            user = User.objects.create_user(
                email = validated_data['email'],
                username = validated_data['username'],
                password = validated_data['password'],
                status = User.StatusChoices.ACTIVE,
                joined_date = validated_data.get('joined_date')
            )
        
            UserProfile.objects.create(user=user)
            role = Role.objects.get(name=role_name)
            UserRole.objects.create(
                user=user,
                role=role
            )
        
        return user