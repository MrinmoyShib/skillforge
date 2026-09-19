"""
Serializers for Admin Submissions Audit & Re-Judge.
"""
from rest_framework import serializers
from apps.submissions.models import Submission, SubmissionResult


class AdminSubmissionResultSerializer(serializers.ModelSerializer):
    is_sample = serializers.BooleanField(source='test_case.is_sample', read_only=True)
    expected_output = serializers.CharField(source='test_case.expected_output', read_only=True)
    input_data = serializers.CharField(source='test_case.input_data', read_only=True)

    class Meta:
        model = SubmissionResult
        fields = [
            'id',
            'order',
            'status',
            'execution_time',
            'memory_usage',
            'actual_output',
            'stderr_output',
            'is_sample',
            'input_data',
            'expected_output',
        ]


class AdminSubmissionListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    problem_title = serializers.CharField(source='problem.title', read_only=True)
    problem_slug = serializers.CharField(source='problem.slug', read_only=True)

    class Meta:
        model = Submission
        fields = [
            'id',
            'user_id',
            'username',
            'problem_id',
            'problem_title',
            'problem_slug',
            'language',
            'status',
            'execution_time',
            'memory_usage',
            'passed_test_cases_count',
            'total_test_cases_count',
            'is_sample_run',
            'created_at',
        ]


class AdminSubmissionDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    problem_title = serializers.CharField(source='problem.title', read_only=True)
    problem_slug = serializers.CharField(source='problem.slug', read_only=True)
    results = AdminSubmissionResultSerializer(many=True, read_only=True)

    class Meta:
        model = Submission
        fields = [
            'id',
            'user_id',
            'username',
            'problem_id',
            'problem_title',
            'problem_slug',
            'language',
            'status',
            'source_code',
            'compile_output',
            'error_message',
            'execution_time',
            'memory_usage',
            'passed_test_cases_count',
            'total_test_cases_count',
            'is_sample_run',
            'results',
            'created_at',
            'updated_at',
        ]

