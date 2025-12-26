from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FCMToken
from .serializers import FCMTokenSerializer
import logging
from rest_framework.decorators import api_view
from .send_notification import sendNotifications
from asgiref.sync import async_to_sync


class RegisterFCMToken(APIView):
    def post(self, request):
        serializer = FCMTokenSerializer(data=request.data)
        if serializer.is_valid():
            device_id = serializer.validated_data['device_id']
            token = serializer.validated_data['token']
            user_id = serializer.validated_data['user_id']
            
            
            # Check if device_id already exists
            existing_token = FCMToken.objects.filter(device_id=device_id).first()
            
            if existing_token:
                message = "Token updated successfully."
            else:
                message = "Token registered successfully."
            
            # Let the serializer handle the create/update logic
            fcm_token = serializer.save()

            sendNotifications(user_id,"Test Notification",message)

            return Response({"message": message}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

