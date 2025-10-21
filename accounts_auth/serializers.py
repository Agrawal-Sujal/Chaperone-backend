from rest_framework import serializers
from accounts.serializers import UserSerializer
from accounts.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'is_walker', 'date_of_birth']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        token, created = Token.objects.get_or_create(user=user)
        return {'token': token.key, 'user': UserSerializer(user).data}
