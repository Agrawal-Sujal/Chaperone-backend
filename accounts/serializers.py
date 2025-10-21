from rest_framework import serializers
from .models import User, Walker, Wanderer, WandererPreferences
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'is_walker', 'date_of_birth']
