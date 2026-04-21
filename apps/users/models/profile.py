from django.db import models
from .user import User


class UserProfile(models.Model):
    
    class GenderChoices(models.TextChoices):
        MALE = 'MALE', 'Male'
        FEMALE = 'FEMALE', 'Female'
        OTHER = 'OTHER', 'Other'
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    full_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True, unique=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices, blank=True)
    avatar_url = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.full_name or self.user.email
    
    