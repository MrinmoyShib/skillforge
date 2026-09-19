"""
Input serializers for authentication and profile management.
"""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

User = get_user_model()


class RegisterInputSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3, max_length=30)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    display_name = serializers.CharField(max_length=150, required=False, allow_blank=True, default='')

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value.lower()

    def validate_password(self, value):
        validate_password(value)
        return value


class LoginInputSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = serializers.CharField(required=False)

    def validate(self, attrs):
        request = self.context.get('request')
        refresh_cookie_name = settings.SIMPLE_JWT.get('REFRESH_COOKIE', 'refresh_token')

        # Read from cookie if not explicitly passed in payload
        token_from_cookie = request.COOKIES.get(refresh_cookie_name) if request else None
        attrs['refresh'] = attrs.get('refresh') or token_from_cookie

        if not attrs.get('refresh'):
            raise exceptions.ValidationError({'refresh': 'No refresh token provided in cookie or payload.'})

        return super().validate(attrs)


class ProfileUpdateInputSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3, max_length=30, required=False)
    email = serializers.EmailField(required=False)
    display_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    phone_number = serializers.CharField(max_length=30, required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    location = serializers.CharField(max_length=100, required=False, allow_blank=True)
    avatar_url = serializers.URLField(required=False, allow_blank=True)
    github_url = serializers.URLField(max_length=255, required=False, allow_blank=True)
    linkedin_url = serializers.URLField(max_length=255, required=False, allow_blank=True)
    twitter_url = serializers.URLField(max_length=255, required=False, allow_blank=True)
    website_url = serializers.URLField(max_length=255, required=False, allow_blank=True)

    def validate_username(self, value):
        user = self.context.get('request').user if self.context.get('request') else None
        qs = User.objects.filter(username__iexact=value)
        if user and user.is_authenticated:
            qs = qs.exclude(id=user.id)
        if qs.exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value

    def validate_email(self, value):
        user = self.context.get('request').user if self.context.get('request') else None
        if user and user.is_authenticated and value.lower().strip() != user.email.lower().strip():
            raise serializers.ValidationError(
                "Direct email change is disabled for security. Please use the 'Change Email' verification feature."
            )
        return value.lower().strip()


class ChangePasswordInputSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = self.context.get('request').user if self.context.get('request') else None
        if not user or not user.is_authenticated:
            raise serializers.ValidationError("User is not authenticated.")

        if not user.check_password(attrs['current_password']):
            raise serializers.ValidationError({"current_password": "Current password is incorrect."})

        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "New passwords do not match."})

        if attrs['new_password'] == attrs['current_password']:
            raise serializers.ValidationError({"new_password": "New password cannot be the same as the current password."})

        validate_password(attrs['new_password'], user=user)
        return attrs


class VerifyOTPInputSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(min_length=6, max_length=6, required=False)
    otp_code = serializers.CharField(min_length=6, max_length=6, required=False)

    def validate(self, attrs):
        code = (attrs.get('otp') or attrs.get('otp_code') or '').strip()
        if not code:
            raise serializers.ValidationError({"otp": "Verification code is required."})
        if not code.isdigit() or len(code) != 6:
            raise serializers.ValidationError({"otp": "Verification code must be 6 digits."})
        attrs['otp'] = code
        attrs['otp_code'] = code
        return attrs


class ResendOTPInputSerializer(serializers.Serializer):
    email = serializers.EmailField()


class RequestEmailChangeInputSerializer(serializers.Serializer):
    new_email = serializers.EmailField()
    current_password = serializers.CharField(write_only=True)

    def validate_new_email(self, value):
        user = self.context.get('request').user if self.context.get('request') else None
        normalized = value.lower().strip()
        if user and user.is_authenticated and normalized == user.email.lower().strip():
            raise serializers.ValidationError("New email must be different from your current email.")
        if User.objects.filter(email__iexact=normalized).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return normalized

    def validate(self, attrs):
        user = self.context.get('request').user if self.context.get('request') else None
        if not user or not user.is_authenticated:
            raise serializers.ValidationError("User is not authenticated.")
        if not user.check_password(attrs['current_password']):
            raise serializers.ValidationError({"current_password": "Current password is incorrect."})
        return attrs


class ConfirmEmailChangeInputSerializer(serializers.Serializer):
    new_email = serializers.EmailField()
    otp = serializers.CharField(min_length=6, max_length=6)

    def validate_new_email(self, value):
        return value.lower().strip()

    def validate_otp(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Verification code must be 6 digits.")
        return value

