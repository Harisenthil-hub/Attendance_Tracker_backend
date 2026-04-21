from django.db import models
from .user import User


class LoginHistory(models.Model):
    
    class LoginStatus(models.TextChoices):
        SUCCESS = 'SUCCESS', 'Success'
        FAILED = 'FAILED', 'Failed'
        LOGGED_OUT = 'LOGGED_OUT', 'Logged Out'
        SESSION_EXPIRED = 'SESSION_EXPIRED', 'Session Expired'
        LOCKED = 'LOCKED', 'Account Locked'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    login_time = models.DateTimeField()
    logout_time = models.DateTimeField(null=True, blank=True)
    
    
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    status = models.CharField(max_length=20, choices=LoginStatus.choices)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class OTPVerification(models.Model):
    
    class OTP_PURPOSE_CHOICES(models.TextChoices):
        PASSWORD_RESET = 'PASSWORD_RESET', 'Password Reset'
        LOGIN = 'LOGIN', 'Login'
        VERIFY_EMAIL = 'VERIFY EMAIL', 'Verify Email'
        
        
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    otp_code = models.CharField(max_length=255)
    purpose = models.CharField(max_length=50, choices=OTP_PURPOSE_CHOICES.choices)
    
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    attempts = models.IntegerField(default=0)
    max_attempts = models.IntegerField(default=5)
    
    created_at = models.DateTimeField(auto_now_add=True)