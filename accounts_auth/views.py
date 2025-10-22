from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from accounts.models import User
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_view(request):
    try:
        email = request.data.get("email")
        password = request.data.get("password")

        user,created = User.objects.get_or_create(email = email, password_hash = password)

        if not created:
            return Response({'error':'This email is already registered.'}, status= status.HTTP_409_CONFLICT)
        
        token,_ = Token.objects.get_or_create(user = user)
        return Response({
            'token':token.key,
            'id': user.id
        },status = status.HTTP_201_CREATED)
    except Exception as e:
        return Response({ "error": str(e)}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    try:
        email = request.data.get("email")
        password = request.data.get("password")

        user = User.objects.get(email = email, password_hash = password)

        if user is None:
            return Response({'error':'Email does not exist or invalid credentials'}, status= status.HTTP_404_NOT_FOUND)
        
        token,_ = Token.objects.get_or_create(user = user)
        return Response({
            'token':token.key,
            'id': user.id
        },status = status.HTTP_200_OK)
   
    except Exception as e:
        return Response({ "error": str(e)}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def google_auth_view(request):

    try:
        credential = request.data.get('id_token')

        payload = id_token.verify_oauth2_token(
            credential,
            requests.Request(),
            settings.GOOGLE_CLIENT_ID
        )

        email = payload.get("email")
        name = payload.get("name", "Unknown User")

        if not email:
            return Response({"error": "Email not available"}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(
            email=email,
            defaults={"name": name, "is_email_verified": True}
        )

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "id": user.id
        }, status=status.HTTP_200_OK)

    except ValueError:
        return Response({"error": "Invalid Google token"}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({ "error": str(e)}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)

