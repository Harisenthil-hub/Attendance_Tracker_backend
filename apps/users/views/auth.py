from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate


from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User
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
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response(
                { 'error': 'Email and password required' },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(request, email=email, password=password)
        
        if user is None:
            return Response(
                { 'error': 'Invalid credentials' },
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        if user.status != User.StatusChoices.ACTIVE:
            return Response(
                { 'error': f'User is {user.status}' },
                status=status.HTTP_403_FORBIDDEN
            )
            
        refresh = RefreshToken.for_user(user)
        
        return Response({ 
                'access': str(refresh.access_token),
                'refresh': str(refresh)
        })