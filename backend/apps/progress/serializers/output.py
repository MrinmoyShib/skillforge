"""
Output serializers for user progress and activity logs.
"""
from rest_framework import serializers
from ..models import ActivityLog


class UserProgressSummaryOutputSerializer(serializers.Serializer):
    username = serializers.CharField()
    display_name = serializers.CharField()
    total_xp = serializers.IntegerField()
    current_level = serializers.IntegerField()
    level_title = serializers.CharField()
    current_level_base_xp = serializers.IntegerField()
    next_level_xp = serializers.IntegerField(allow_null=True)
    progress_percent = serializers.FloatField()
    problems_solved_count = serializers.IntegerField()
    current_streak_days = serializers.IntegerField()
    last_solve_date = serializers.DateField(allow_null=True)


class UserSolvedProblemsOutputSerializer(serializers.Serializer):
    solved_problem_ids = serializers.ListField(child=serializers.IntegerField())
    total_solved = serializers.IntegerField()


class ActivityLogOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = [
            'id',
            'activity_type',
            'description',
            'metadata',
            'created_at',
        ]

