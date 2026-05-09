from rest_framework import serializers
from apps.users.models import OTPVerification

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
    reset_token = serializers.CharField()
    new_password = serializers.CharField()