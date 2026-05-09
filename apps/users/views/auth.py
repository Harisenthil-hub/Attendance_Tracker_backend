from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate


from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User, LoginHistory
from apps.users.serializers.auth import RegisterSerializer


class RegisterView(APIView):
    
    def post(self, request):
        
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'User created successfully'},
                status=status.HTTP_201_CREATED
            )
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    
    def post(self, request):
        login = request.data.get('login')
        password = request.data.get('password')
        
        if not login or not password:
            return Response(
                { 'error': 'Email and password required' },
                status=status.HTTP_400_BAD_REQUEST
            )
            
        user_obj = User.objects.filter(email=login).first()
        
        if not user_obj:
            user_obj = User.objects.filter(username=login).first()
        
        
        if not user_obj:
            return Response(
                { 'error': 'Invalid credentials' },
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        user = authenticate(request, email=user_obj.email, password=password)
        
        
        if user is None:
            
            LoginHistory.objects.create(
                user=user_obj,
                action=LoginHistory.ActionChoices.LOGIN_FAILED,
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            return Response(
                { 'error': 'Invalid credentials' },
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        if user.status != User.StatusChoices.ACTIVE:
            LoginHistory.objects.create(
                user=user_obj,
                action=LoginHistory.ActionChoices.ACCOUNT_LOCKED,
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            return Response(
                { 'error': f'User is {user.status}' },
                status=status.HTTP_403_FORBIDDEN
            )
            
        
        LoginHistory.objects.create(
            user=user_obj,
            action=LoginHistory.ActionChoices.LOGIN_SUCCESS,
            ip_address=self.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        refresh = RefreshToken.for_user(user)
        
        return Response({ 
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        })
        
        
    def get_client_ip(self, request):
        
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        
        return request.META.get('REMOTE_ADDR')
        
        
        