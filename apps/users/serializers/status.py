from rest_framework import serializers


class UpdateStatusSerializer(serializers.Serializer):
    
    new_status = serializers.ChoiceField(
        choices=['ACTIVE', 'INACTIVE', 'SUSPENDED', 'TERMINATED']
    )
    
    suspension_reason = serializers.CharField(required=False, allow_blank=True)
    suspension_start = serializers.DateTimeField(required=False)
    suspension_end = serializers.DateTimeField(required=False)
    
    termination_reason = serializers.CharField(required=False, allow_blank=True)
    terminated_at = serializers.DateTimeField(required=False)
    
    