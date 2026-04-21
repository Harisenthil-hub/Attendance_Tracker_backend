import random
from django.utils import timezone
from datetime import timedelta
from apps.users.models import OTPVerification


def generate_otp():
    return str(random.randint(100000,999999))


def create_otp(user, purpose):
    otp = generate_otp()
    
    OTPVerification.objects.create(
        user=user,
        otp_code=otp, # later want hash this
        purpose=purpose,
        expires_at=timezone.now() + timedelta(minutes=5),
        attempts=0
    )
    
    return otp