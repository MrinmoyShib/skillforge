"""
Output serializers for the public developer portfolio view.
"""
from rest_framework import serializers


class PortfolioUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    display_name = serializers.CharField()
    current_level = serializers.IntegerField()
    level_title = serializers.CharField()
    total_xp = serializers.IntegerField()
    problems_solved_count = serializers.IntegerField()
    current_streak_days = serializers.IntegerField()
    bio = serializers.CharField(allow_blank=True)
    avatar_url = serializers.CharField(allow_blank=True, default='')
    phone_number = serializers.CharField(allow_blank=True, default='')
    github_url = serializers.CharField(allow_blank=True, default='')
    linkedin_url = serializers.CharField(allow_blank=True, default='')
    twitter_url = serializers.CharField(allow_blank=True, default='')
    website_url = serializers.CharField(allow_blank=True, default='')
    joined_at = serializers.DateTimeField()


class PortfolioTrackSerializer(serializers.Serializer):
    slug = serializers.CharField()
    name = serializers.CharField()
    total_problems = serializers.IntegerField()
    solved_problems = serializers.IntegerField()
    xp_earned = serializers.IntegerField()
    mastery_percent = serializers.FloatField()


class PortfolioVerifiedProjectSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    slug = serializers.CharField()
    language = serializers.CharField()
    difficulty = serializers.CharField()
    short_description = serializers.CharField()
    technologies = serializers.ListField(child=serializers.CharField(), default=list)
    xp_reward = serializers.IntegerField()
    completed_at = serializers.DateTimeField()


class PortfolioSkillDomainSerializer(serializers.Serializer):
    slug = serializers.CharField()
    name = serializers.CharField()
    solved_count = serializers.IntegerField()


class PortfolioAchievementSerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField()
    icon = serializers.CharField()
    badge_type = serializers.CharField()
    unlocked_at = serializers.DateTimeField()


class PortfolioActivitySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    activity_type = serializers.CharField()
    description = serializers.CharField()
    created_at = serializers.DateTimeField()


class PortfolioDetailOutputSerializer(serializers.Serializer):
    user = PortfolioUserSerializer()
    tracks = PortfolioTrackSerializer(many=True)
    verified_projects = PortfolioVerifiedProjectSerializer(many=True)
    skill_domains = PortfolioSkillDomainSerializer(many=True)
    achievements = PortfolioAchievementSerializer(many=True)
    recent_activity = PortfolioActivitySerializer(many=True)

