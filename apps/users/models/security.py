from django.db import models
from .user import User
from django.utils import timezone

class LoginHistory(models.Model):
    
    class ActionChoices(models.TextChoices):
        LOGIN_SUCCESS = 'LOGIN_SUCCESS', 'Login Success'
        LOGIN_FAILED = 'LOGIN_FAILED', 'Login Failed'
        LOGGED_OUT = 'LOGGED_OUT', 'Logged Out'
        SESSION_EXPIRED = 'SESSION_EXPIRED', 'Session Expired'
        ACCOUNT_LOCKED = 'ACCOUNT_LOCKED', 'Account Locked'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # login_time = models.DateTimeField()
    # logout_time = models.DateTimeField(null=True, blank=True)
    
    action = models.CharField(max_length=30, choices=ActionChoices.choices)
    
    
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    # status = models.CharField(max_length=20, choices=LoginStatus.choices)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class OTPVerification(models.Model):
    
    class OTPPurposeChoices(models.TextChoices):
        PASSWORD_RESET = 'PASSWORD_RESET', 'Password Reset'
        LOGIN = 'LOGIN', 'Login'
        VERIFY_EMAIL = 'VERIFY_EMAIL', 'Verify Email'
        
    class OTPStatus(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        USED = 'USED', 'Used'
        EXPIRED = 'EXPIRED', 'Expired'
        INVALIDATED = 'INVALIDATED', 'Invalidated'
        MAX_ATTEMPTS_EXCEEDED = 'MAX_ATTEMPTS_EXCEEDED', 'Max Attempts Exceeded'
          
        
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    otp_code = models.CharField(max_length=255)
    purpose = models.CharField(max_length=50, choices=OTPPurposeChoices.choices)
    
    expires_at = models.DateTimeField()
    # is_used = models.BooleanField(default=False)
    status = models.CharField(max_length=30, choices=OTPStatus.choices, default=OTPStatus.ACTIVE)
    
    attempts = models.IntegerField(default=0)
    max_attempts = models.IntegerField(default=5)
    
    reset_token = models.CharField(max_length=255, null=True, blank=True)
    reset_token_expires_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    @classmethod
    def invalidate_old_otps(cls, user, purpose):
        cls.objects.filter(
            user=user,
            purpose=purpose,
            status=cls.OTPStatus.ACTIVE
        ).update(status=cls.OTPStatus.INVALIDATED)
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def has_exceeded_attempts(self):
        return self.attempts >= self.max_attempts
    
    def increment_attempts(self):
        self.attempts += 1
        self.save(update_fields=['attempts'])
        
    