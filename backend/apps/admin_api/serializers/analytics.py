"""
Serializers for Admin Platform Analytics & Telemetry.
"""
from rest_framework import serializers


class SystemHealthSerializer(serializers.Serializer):
    database = serializers.CharField()
    sandbox = serializers.CharField()
    redis = serializers.CharField()


class LanguageSolvesSerializer(serializers.Serializer):
    python = serializers.IntegerField(default=0)
    javascript = serializers.IntegerField(default=0)
    cpp = serializers.IntegerField(default=0)


class AdminAnalyticsOutputSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    active_users = serializers.IntegerField()
    staff_users = serializers.IntegerField()
    
    total_problems = serializers.IntegerField()
    published_problems = serializers.IntegerField()
    draft_problems = serializers.IntegerField()
    total_test_cases = serializers.IntegerField()
    
    total_projects = serializers.IntegerField()
    total_milestones_completed = serializers.IntegerField()
    
    total_submissions = serializers.IntegerField()
    accepted_submissions = serializers.IntegerField()
    acceptance_rate = serializers.FloatField()
    
    solves_by_language = LanguageSolvesSerializer()
    system_health = SystemHealthSerializer()

