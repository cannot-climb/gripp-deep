from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=128, write_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username: str = data.get("username", None)
        password: str = data.get("password", None)
        user = authenticate(username=username, password=password)

        if user is None:
            return {
                "username": "None",
                "refresh_token": str(None),
                "access_token": str(None),
            }

        refresh = RefreshToken.for_user(user)

        return {
            "username": user.username,
            "refresh_token": str(refresh),
            "access_token": str(refresh.access_token),
        }
