from rest_framework import serializers

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate(self, attrs):
        password = attrs.get('password', '')

        if not password.isalnum():
            raise serializers.ValidationError('username must be string and integer')

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)