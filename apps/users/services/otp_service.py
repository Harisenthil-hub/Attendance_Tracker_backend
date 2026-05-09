import random
from django.utils import timezone
from datetime import timedelta
from apps.users.models import OTPVerification
from django.contrib.auth.hashers import make_password
import secrets


def generate_otp():
    return str(secrets.randbelow(900000) + 100000)

def create_otp(user, purpose):
    otp = generate_otp()
    
    OTPVerification.invalidate_old_otps(
        user=user,
        purpose=purpose
    )
    
    OTPVerification.objects.create(
        user=user,
        otp_code=make_password(otp),
        purpose=purpose,
        expires_at=timezone.now() + timedelta(minutes=3),
        attempts=0
    )
    
    return otp