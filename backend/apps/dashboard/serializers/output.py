"""
Output serializers for the aggregated dashboard payload.
"""
from rest_framework import serializers
from apps.progress.serializers.output import UserProgressSummaryOutputSerializer


class DashboardCategoryMasterySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.CharField()
    total_problems = serializers.IntegerField()
    solved_problems = serializers.IntegerField()
    remaining_problems = serializers.IntegerField(default=0)
    xp_earned = serializers.IntegerField(default=0)
    total_xp = serializers.IntegerField(default=0)
    mastery_percent = serializers.FloatField()
    beginner_total = serializers.IntegerField(default=0)
    beginner_solved = serializers.IntegerField(default=0)
    intermediate_total = serializers.IntegerField(default=0)
    intermediate_solved = serializers.IntegerField(default=0)
    master_total = serializers.IntegerField(default=0)
    master_solved = serializers.IntegerField(default=0)
    next_unsolved_slug = serializers.CharField(allow_null=True, required=False, default=None)


class DashboardRecentSubmissionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    problem_id = serializers.IntegerField()
    problem_title = serializers.CharField()
    problem_slug = serializers.CharField()
    language = serializers.CharField(default='cpp')
    difficulty = serializers.CharField()
    status = serializers.CharField()
    execution_time = serializers.FloatField(allow_null=True)
    memory_usage = serializers.IntegerField(allow_null=True)
    passed_cases = serializers.IntegerField()
    total_cases = serializers.IntegerField()
    is_sample_run = serializers.BooleanField()
    created_at = serializers.DateTimeField()


class DashboardRecommendedProblemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    slug = serializers.CharField()
    category_name = serializers.CharField()
    language = serializers.CharField(default='cpp')
    difficulty = serializers.CharField()
    challenge_level = serializers.IntegerField()
    xp_reward = serializers.IntegerField()


class DashboardActivitySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    activity_type = serializers.CharField()
    description = serializers.CharField()
    metadata = serializers.DictField()
    created_at = serializers.DateTimeField()


class DashboardEnrolledProjectSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    slug = serializers.CharField()
    language = serializers.CharField()
    difficulty = serializers.CharField()
    status = serializers.CharField()
    current_milestone_order = serializers.IntegerField()
    completed_milestones_count = serializers.IntegerField()
    total_milestones_count = serializers.IntegerField()
    progress_percent = serializers.FloatField()
    xp_reward = serializers.IntegerField()
    started_at = serializers.DateTimeField(allow_null=True)
    completed_at = serializers.DateTimeField(allow_null=True)


class DashboardDataOutputSerializer(serializers.Serializer):
    stats = UserProgressSummaryOutputSerializer()
    category_mastery = DashboardCategoryMasterySerializer(many=True)
    recent_submissions = DashboardRecentSubmissionSerializer(many=True)
    recommended_problems = DashboardRecommendedProblemSerializer(many=True)
    recent_activity = DashboardActivitySerializer(many=True)
    enrolled_projects = DashboardEnrolledProjectSerializer(many=True, default=list)

