from rest_framework import serializers
from apps.users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        
    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value
    
    def create(self, validated_data):
        
        user = User.objects.create_user(
            email = validated_data['email'],
            username = validated_data['username'],
            password = validated_data['password'],
            status = User.StatusChoices.ACTIVE
        )
        
        return user