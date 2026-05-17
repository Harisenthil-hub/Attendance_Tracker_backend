from rest_framework import serializers
from apps.users.models import OTPVerification
from django.contrib.auth.password_validation import validate_password

class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    purpose = serializers.ChoiceField(
        choices=OTPVerification.OTPPurposeChoices.choices
    )
    

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    purpose = serializers.ChoiceField(
        choices=OTPVerification.OTPPurposeChoices.choices
    )
    otp = serializers.CharField()
    
class ResetPasswordSerializer(serializers.Serializer):
    token_identifier = serializers.UUIDField()
    reset_token = serializers.CharField()
    new_password = serializers.CharField()
    
    def validate_new_password(self, value):
        validate_password(value)
        
        return value