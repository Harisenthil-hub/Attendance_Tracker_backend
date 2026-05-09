from rest_framework import serializers
from apps.users.models import User, UserProfile


class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = ['full_name', 'phone', 'dob', 'gender', 'avatar_url']

class UserSerializer(serializers.ModelSerializer):
    
    profile = ProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['uuid', 'username', 'email', 'status', 'is_verified', 'profile']
        read_only_fields = [ 'uuid', 'username', 'status', 'is_verified' ]