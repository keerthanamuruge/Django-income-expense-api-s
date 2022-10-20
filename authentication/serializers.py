from rest_framework import serializers

from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed


class RegisterSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def validate(self, attrs):
        password = attrs.get('password', '')

        if not password.isalnum():
            raise serializers.ValidationError('username must be string and integer')

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, min_length=6, read_only=True)
    tokens = serializers.defaultdict()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'tokens']

    def validate(self, attr):
        password = attr.get('password')
        email = attr.get('email')

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credential')

        if not user.is_active:
            raise AuthenticationFailed('Account is disabled, please contact admin')

        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'tokens': user.tokens()
        }


class VerifyEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email']


class EmailVerification(serializers.ModelSerializer):
    token = serializers.CharField(write_only=True)