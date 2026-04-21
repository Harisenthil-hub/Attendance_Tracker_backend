from django.db import models
from .user import User


class UserStatusDetails(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='status_details')
    
    suspension_reason = models.TextField(blank=True)
    suspension_start = models.DateTimeField(null=True, blank=True)
    suspension_end = models.DateTimeField(null=True, blank=True)
    
    termination_reason = models.TextField(blank=True)
    terminated_at = models.DateTimeField(null=True, blank=True)
    
class UserStatusHistory(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='status_history')
    
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    
    reason = models.TextField(blank=True)
    
    changed_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='changed_users')
    
    changed_at = models.DateTimeField(auto_now_add=True)
    
    
    