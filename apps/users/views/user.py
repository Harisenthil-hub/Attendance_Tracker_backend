from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from apps.users.models import UserStatusDetails, UserStatusHistory
from apps.users.serializers.user import UserSerializer, ProfileSerializer


class MeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        # print(user)
        data = UserSerializer(user).data
        
        return Response(data, status=status.HTTP_200_OK)
    
    def patch(self, request):
        
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    

class UpdateProfile(APIView):
    permission_classes = [IsAuthenticated]
    
    
    def patch(self, request):
        
        profile = request.user.profile
        
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        