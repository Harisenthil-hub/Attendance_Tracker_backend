from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework.response import Response
from rest_framework import status


class CookieTokenRefreshView(TokenRefreshView):
    
    def post(self, request, *args, **kwargs):
        
        refresh_token = request.COOKIES.get('refresh_token')
        
        if not refresh_token:
            return Response({
                'success': False,
                'error': 'No refresh token'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        
        serializer = TokenRefreshSerializer(
            data={
                'refresh': refresh_token
            }
        )
        
        serializer.is_valid(raise_exception=True)
        
        access_token = serializer.validated_data['access']
        new_refresh_token = serializer.validated_data.get('refresh')
        
        
        response =  Response(
            {
                'success': True,
                'message': 'New access and refresh token has been created'
            }
        , status=status.HTTP_200_OK)
        
        
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=False,
            samesite='Lax'
        )
        
        if new_refresh_token:
            
            response.set_cookie(
            key='refresh_token',
            value=new_refresh_token,
            httponly=True,
            secure=False,
            samesite='Lax'
        )
        
        return response