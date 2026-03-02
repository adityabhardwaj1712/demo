from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "job_title", "timezone"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        identifier = data.get("username_or_email")
        password = data.get("password")

        user = None

        # Try username first
        user = authenticate(username=identifier, password=password)

        # If not found, try email
        if not user:
            try:
                user_obj = User.objects.get(email__iexact=identifier)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass

        if not user:
            raise serializers.ValidationError("Invalid username/email or password")

        data["user"] = user
        return data