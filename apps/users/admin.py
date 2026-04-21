from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(UserStatusDetails)
admin.site.register(UserStatusHistory)

admin.site.register(Role)
admin.site.register(UserRole)

admin.site.register(Permission)
admin.site.register(RolePermission)

admin.site.register(LoginHistory)
admin.site.register(OTPVerification)