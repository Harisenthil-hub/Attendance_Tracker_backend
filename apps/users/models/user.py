from uuid6 import uuid7
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from apps.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    class StatusChoices(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        INACTIVE = 'INACTIVE', 'Inactive'
        SUSPENDED = 'SUSPENDED', 'Suspended'
        TERMINATED = 'TERMINATED', 'Terminated'
        
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid7, unique=True, editable=True)
    
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True, max_length=254)
    password = models.CharField(max_length=255)
    
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.ACTIVE)
    
    is_verified = models.BooleanField(default=False)
    
    last_login = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
        