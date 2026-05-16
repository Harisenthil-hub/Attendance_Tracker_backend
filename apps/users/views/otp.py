from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from apps.users.models import User, OTPVerification
from apps.users.serializers.otp import *
from apps.users.services.otp_service import create_otp


import secrets
from datetime import timedelta
from django.contrib.auth.hashers import check_password, make_password



class SendOTPView(APIView):
    
    permission_classes = []
    authentication_classes = []
    
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data['email']
        purpose = serializer.validated_data['purpose']
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response( { 'message': 'If account exists, OTP has been sent' }, status=status.HTTP_200_OK )
        
        
        otp = create_otp(user, purpose)
        
        
        print('Otp:', otp) # here otp sending logic will come
        
        return Response({ 'message': 'If account exists, OTP has been sent' }, status=status.HTTP_200_OK)
    
    
class VerifyOTPView(APIView):
    
    permission_classes = []
    authentication_classes = []
    
    def post(self, request):
        
        serializer = VerifyOTPSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        purpose = serializer.validated_data['purpose']
        
        
        try:
            user = User.objects.get(email=email)
            otp_obj = OTPVerification.objects.filter(
                user=user,
                purpose=purpose,
                status=OTPVerification.OTPStatus.ACTIVE
            ).latest('created_at')
            
        except (User.DoesNotExist, OTPVerification.DoesNotExist):
            return Response({ 'error': 'Invalid OTP' }, status=status.HTTP_400_BAD_REQUEST)
        
        
        if otp_obj.is_expired():
            otp_obj.status = OTPVerification.OTPStatus.EXPIRED
            otp_obj.save(update_fields=['status'])
            return Response({ 'error': 'OTP Expired' }, status=status.HTTP_400_BAD_REQUEST)
        
        
        if otp_obj.has_exceeded_attempts():
            otp_obj.status = OTPVerification.OTPStatus.MAX_ATTEMPTS_EXCEEDED
            otp_obj.save(update_fields=['status'])
            return Response({ 'error': 'Maximum OTP attempts exceeded' }, status=status.HTTP_403_FORBIDDEN)
            
        if not check_password(otp, otp_obj.otp_code):
            otp_obj.increment_attempts()
            
            if otp_obj.has_exceeded_attempts():
                otp_obj.status = OTPVerification.OTPStatus.MAX_ATTEMPTS_EXCEEDED
                otp_obj.save(update_fields=['status'])
                return Response({ 'error': 'Maximum OTP attempts exceeded' }, status=status.HTTP_403_FORBIDDEN)
                
            
            remaining_attempts = (otp_obj.max_attempts - otp_obj.attempts)
            return Response(
                { 
                    'error': 'Wrong OTP',
                    'remaining_attempts': remaining_attempts
                }
            , status=status.HTTP_400_BAD_REQUEST)
        
        raw_token = secrets.token_urlsafe(32)
        hashed_reset_token = make_password(raw_token)
        
        otp_obj.status = OTPVerification.OTPStatus.USED
        otp_obj.reset_token = hashed_reset_token
        otp_obj.reset_token_expires_at = timezone.now() + timedelta(minutes=10)
        otp_obj.save()
        
        return Response(
            { 
                'message': 'OTP Verified',
                'token_identifier': otp_obj.token_identifier,
                'reset_token': raw_token,
            }
        )
           

class ResetPasswordView(APIView):
    
    permission_classes = []
    authentication_classes = []
    
    def post(self, request):
        
        serializer = ResetPasswordSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        reset_token = serializer.validated_data['reset_token']
        new_password = serializer.validated_data['new_password']
        token_identifier = serializer.validated_data['token_identifier']
        
        
        try:
            otp_obj = OTPVerification.objects.get(
                token_identifier=token_identifier,
                status=OTPVerification.OTPStatus.USED
            )
        except OTPVerification.DoesNotExist:
            return Response({ 'error': 'Invalid reset token' }, status=status.HTTP_400_BAD_REQUEST)
        
        
        if not check_password(reset_token, otp_obj.reset_token):
            return Response({ 'error': 'Invalid Token' }, status=status.HTTP_400_BAD_REQUEST)
        
        if ( not otp_obj.reset_token_expires_at or 
            otp_obj.reset_token_expires_at < timezone.now()
            ):
            return Response({ 'error': 'Reset token expired' }, status=status.HTTP_400_BAD_REQUEST)
        
        
        user = otp_obj.user
        
        user.set_password(new_password)
        user.save()
        
        # invalidate token
        otp_obj.reset_token = None
        otp_obj.reset_token_expires_at = None
        otp_obj.status = OTPVerification.OTPStatus.INVALIDATED
        otp_obj.save(
            update_fields=[
                'reset_token',
                'reset_token_expires_at',
                'status'
            ]
        )
        
        return Response({ 'message': 'Password reset successfull' }, status=status.HTTP_200_OK)
        