from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from django.utils import timezone

from apps.users.models import User, UserStatusDetails, UserStatusHistory
from apps.users.serializers.status import UpdateStatusSerializer


class UpdateUserStatusView(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, user_uuid):
        
        serializer = UpdateStatusSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(uuid=user_uuid)
        except User.DoesNotExist:
            return Response({ 'error': 'User not found' }, status=status.HTTP_404_NOT_FOUND)
        
        
        new_status = serializer.validated_data['new_status']
        
        reason = (
            serializer.validated_data.get('suspension_reason') or 
            serializer.validated_data.get('termination_reason')
        )
        
        suspension_start = serializer.validated_data.get('suspension_start')
        suspension_end = serializer.validated_data.get('suspension_end') 
        terminated_at = serializer.validated_data.get('terminated_at')
        
        
        old_status = user.status
        
        # Updating user status
        user.status = new_status
        user.save()
        
        # update details table
        
        details, _ = UserStatusDetails.objects.get_or_create(user=user)
        
        if new_status == 'SUSPENDED':
            details.suspension_reason = reason
            details.suspension_start = suspension_start
            details.suspension_end = suspension_end
        elif new_status == 'TERMINATED':
            details.termination_reason = reason
            details.terminated_at = terminated_at
            
        details.save()
        
        # History logging
        UserStatusHistory.objects.create(
            user=user,
            old_status=old_status,
            new_status=new_status,
            reason=reason,
            changed_by=request.user
        )
        
        return Response({ 'message': 'Status updated successfully' }, status=status.HTTP_200_OK)
            
        
