from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from apps.users.models import UserStatusDetails, UserStatusHistory
from apps.users.serializers.user import CurrentUserSerializer, ProfileSerializer


class MeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        # print(user)
        data = CurrentUserSerializer(user).data
        
        return Response(
            {
                'success': True,
                'user': data
            },
            status=status.HTTP_200_OK)
    
    def patch(self, request):
        
        profile = request.user.profile
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'success': True,
                    'message': 'Profile updated successfully',
                    'profile': serializer.data
                }, 
                status=status.HTTP_200_OK)
        return Response({
            'success': False,
            'error': serializer.errors 
        }, status=status.HTTP_400_BAD_REQUEST)
     
        