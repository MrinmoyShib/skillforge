"""
Output presentation serializers for authentication and user profiles.
"""
from rest_framework import serializers


class UserProfileOutputSerializer(serializers.Serializer):
    display_name = serializers.CharField()
    avatar_url = serializers.CharField(allow_blank=True)
    bio = serializers.CharField(allow_blank=True)
    location = serializers.CharField(allow_blank=True)
    phone_number = serializers.CharField(allow_blank=True)
    github_url = serializers.CharField(allow_blank=True)
    linkedin_url = serializers.CharField(allow_blank=True)
    twitter_url = serializers.CharField(allow_blank=True)
    website_url = serializers.CharField(allow_blank=True)
    total_xp = serializers.IntegerField()
    current_level = serializers.IntegerField()
    problems_solved_count = serializers.IntegerField()
    current_streak_days = serializers.IntegerField()
    last_solve_date = serializers.DateField(allow_null=True)
    created_at = serializers.DateTimeField()


class UserOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField()
    is_staff = serializers.BooleanField()
    date_joined = serializers.DateTimeField()
    profile = UserProfileOutputSerializer(read_only=True)


class AuthMessageOutputSerializer(serializers.Serializer):
    detail = serializers.CharField()
    user = UserOutputSerializer(required=False, allow_null=True)


class CSRFOutputSerializer(serializers.Serializer):
    detail = serializers.CharField()
    csrfToken = serializers.CharField()

