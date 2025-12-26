from rest_framework import serializers
from .models import FCMToken

class FCMTokenSerializer(serializers.Serializer):
    device_id = serializers.CharField(max_length=100)
    token = serializers.CharField(max_length=255)
    user_id = serializers.IntegerField()
    
    def create(self, validated_data):
        device_id = validated_data.get('device_id')
        token = validated_data.get('token')
        user_id = validated_data.get('user_id')
        
        # Use update_or_create to handle both create and update cases
        fcm_token, created = FCMToken.objects.update_or_create(
            device_id=device_id,
            defaults={
                'token': token,
                'user_id': user_id
            }
        )
        return fcm_token
