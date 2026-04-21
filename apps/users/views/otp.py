from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from apps.users.models import User, OTPVerification
from apps.users.serializers.otp import *
from apps.users.services.otp_service import create_otp



class SendOTPView(APIView):
    
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data['email']
        purpose = serializer.validated_data['purpose']
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response( { 'error': 'User account not found' }, status=status.HTTP_404_NOT_FOUND )
        
        
        otp = create_otp(user, purpose)
        
        
        print('Otp:', otp) # here otp sending logic will come
        
        return Response({ 'message': 'OTP has been sent' }, status=status.HTTP_200_OK)
    
    
class VerifyOTPView(APIView):
    
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
                is_used=False
            ).latest('created_at')
            
        except:
            return Response({ 'error': 'Invalid OTP' }, status=status.HTTP_400_BAD_REQUEST)
        
        
        if otp_obj.expires_at < timezone.now():
            return Response({ 'error': 'OTP Expired' }, status=status.HTTP_400_BAD_REQUEST)
        
        if otp_obj.otp_code != otp:
            otp_obj.attempts +=  1
            otp_obj.save()
            return Response({ 'error': 'Wrong OTP' }, status=status.HTTP_400_BAD_REQUEST)
        
        
        otp_obj.is_used = True
        otp_obj.save()
        
        return Response({ 'message': 'OTP Verified' })
            

class ResetPasswordView(APIView):
    
    def post(self, request):
        
        serializer = ResetPasswordSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        new_password = serializer.validated_data['new_password']
        
        
        try:
            user = User.objects.get(email=email)
            otp_obj = OTPVerification.objects.filter(
                user=user,
                otp_code=otp,
                is_used=True
            )
        except:
            return Response({ 'error': 'Invalid OTP' }, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(password)
        user.save()
        
        return Response({ 'message': 'Password reset successfull' }, status=status.HTTP_201_CREATED)
        