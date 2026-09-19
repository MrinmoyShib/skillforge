"""
Output serializers for Leaderboard rankings.
"""
from rest_framework import serializers


class LeaderboardEntrySerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    display_name = serializers.CharField()
    avatar_initial = serializers.CharField()
    level = serializers.IntegerField()
    level_title = serializers.CharField()
    total_xp = serializers.IntegerField()
    problems_solved_count = serializers.IntegerField()
    current_streak_days = serializers.IntegerField()
    is_current_user = serializers.BooleanField()


class LeaderboardResponseSerializer(serializers.Serializer):
    results = LeaderboardEntrySerializer(many=True)
    total_count = serializers.IntegerField()
    current_user_rank = serializers.IntegerField(allow_null=True)

