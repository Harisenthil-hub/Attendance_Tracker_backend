from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import User, LoginHistory, UserRole
from apps.users.serializers.auth import CreateUserSerializer
from apps.users.services.permission_service import has_permission
from apps.users.permissions.rbac import HasRBACPermission
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone




class CreateUserView(APIView):
    
    permission_classes = [IsAuthenticated, HasRBACPermission]
    required_permission = 'create_user'
    
    def post(self, request):
        
        requested_role = request.data.get('role')
        
        
        if requested_role == 'admin':
            if not has_permission(request.user, 'create_admin'):
                return Response(
                    { 'error': 'No permission to create admin' },
                    status=status.HTTP_403_FORBIDDEN
                )
                
        
        if requested_role == 'teamlead':
            if not has_permission(request.user, 'create_teamlead'):
                return Response(
                    { 'error': 'No permission to create Team lead' },
                    status=status.HTTP_403_FORBIDDEN
                )
                
                
        
        
        serializer = CreateUserSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {'message': 'User created successfully'},
                status=status.HTTP_201_CREATED
            )
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        login = request.data.get('login')
        password = request.data.get('password')
        
        if not login or not password:
            return Response(
                { 
                    'success': False,
                    'error': 'Email/username and password required'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
            
        user_obj = User.objects.filter(email=login).first()
        
        if not user_obj:
            user_obj = User.objects.filter(username=login).first()
        
        
        if not user_obj:
            return Response(
                { 
                    'success': False,
                    'error': 'Invalid credentials'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        user = authenticate(request, username=user_obj.email, password=password)
        
        
        if user is None:
            
            LoginHistory.objects.create(
                user=user_obj,
                action=LoginHistory.ActionChoices.LOGIN_FAILED,
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            return Response(
                {
                    'success': False,
                    'error': 'Invalid credentials'
                },
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
                {
                    'success': False,
                    'error': f'User is {user.status}'
                },
                status=status.HTTP_403_FORBIDDEN
            )
            
            
        # Here want to add verified logic in future
        
        
        
        #  Update last login
        
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        
        LoginHistory.objects.create(
            user=user_obj,
            action=LoginHistory.ActionChoices.LOGIN_SUCCESS,
            ip_address=self.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        refresh = RefreshToken.for_user(user)
        
        
        # Getting active role
        
        active_role = UserRole.objects.filter(
            user=user,
            removed_at__isnull=True
        ).select_related('role').first()
        
        role_name = None
        
        if active_role:
            role_name = active_role.role.name
        
        response =  Response({ 
            'success': True,
            'message': 'Login successfull',
            'user': {
                'uuid': str(user.uuid),
                'username': user.username,
                'email': user.email,
                'role': role_name   
            }
        }, status=status.HTTP_200_OK)
        
        
        response.set_cookie(
            key='access_token',
            value=str(refresh.access_token),
            httponly=True,
            secure=False,
            samesite='Lax'
        )
        
        
        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite='Lax'
        )
        
        return response
        
        
    def get_client_ip(self, request):
        
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        
        return request.META.get('REMOTE_ADDR')
        
        
        