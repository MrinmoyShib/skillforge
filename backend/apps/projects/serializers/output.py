"""
Output presentation serializers for Guided Projects and Milestones.
"""
from rest_framework import serializers


class ProjectMilestoneOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    order = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    starter_code = serializers.CharField()
    hints = serializers.ListField(child=serializers.CharField(), default=list)
    xp_reward = serializers.IntegerField()


class UserProjectProgressOutputSerializer(serializers.Serializer):
    status = serializers.CharField()
    current_milestone_order = serializers.IntegerField()
    completed_milestones = serializers.ListField(child=serializers.IntegerField(), default=list)
    submitted_code = serializers.DictField(default=dict)
    started_at = serializers.DateTimeField()
    completed_at = serializers.DateTimeField(allow_null=True)


class ProjectListOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    slug = serializers.CharField()
    language = serializers.CharField()
    difficulty = serializers.CharField()
    challenge_level = serializers.IntegerField()
    short_description = serializers.CharField()
    technologies = serializers.ListField(child=serializers.CharField(), default=list)
    xp_reward = serializers.IntegerField()
    estimated_minutes = serializers.IntegerField()
    milestones_count = serializers.IntegerField(default=0)
    user_status = serializers.CharField(default='NOT_STARTED')
    completed_milestones_count = serializers.IntegerField(default=0)


class ProjectDetailOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    slug = serializers.CharField()
    language = serializers.CharField()
    difficulty = serializers.CharField()
    challenge_level = serializers.IntegerField()
    short_description = serializers.CharField()
    description = serializers.CharField()
    technologies = serializers.ListField(child=serializers.CharField(), default=list)
    starter_files = serializers.DictField(default=dict)
    xp_reward = serializers.IntegerField()
    estimated_minutes = serializers.IntegerField()
    milestones = ProjectMilestoneOutputSerializer(many=True)
    user_progress = UserProjectProgressOutputSerializer(allow_null=True, required=False)


class MilestoneVerificationResultSerializer(serializers.Serializer):
    passed = serializers.BooleanField()
    message = serializers.CharField()
    compile_output = serializers.CharField(allow_blank=True, default='')
    execution_time = serializers.FloatField(allow_null=True, default=None)
    xp_awarded = serializers.IntegerField(default=0)
    project_completed = serializers.BooleanField(default=False)
    next_milestone_order = serializers.IntegerField(allow_null=True, default=None)

