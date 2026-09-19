"""
Output serializers for the Achievements API.
"""
from rest_framework import serializers


class AchievementOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.CharField()
    description = serializers.CharField()
    icon = serializers.CharField()
    criteria_type = serializers.CharField()
    criteria_value = serializers.IntegerField()
    xp_bonus = serializers.IntegerField()
    is_unlocked = serializers.BooleanField()
    earned_at = serializers.DateTimeField(allow_null=True)
    current_progress = serializers.IntegerField()
    progress_percent = serializers.FloatField()

