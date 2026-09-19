"""
Output presentation serializers for Submissions and Results.
Enforces test case sanitization to protect hidden evaluation cases from leaking.
"""
from rest_framework import serializers


class SubmissionResultOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    order = serializers.IntegerField()
    status = serializers.CharField()
    execution_time = serializers.FloatField(allow_null=True)
    memory_usage = serializers.IntegerField(allow_null=True)
    is_sample = serializers.SerializerMethodField()
    input_data = serializers.SerializerMethodField()
    expected_output = serializers.SerializerMethodField()
    actual_output = serializers.SerializerMethodField()
    stderr_output = serializers.CharField(allow_blank=True)

    def get_is_sample(self, obj) -> bool:
        return obj.test_case.is_sample

    def _can_view_data(self, obj) -> bool:
        request = self.context.get('request')
        is_staff = bool(request and request.user and request.user.is_staff)
        return obj.test_case.is_sample or is_staff

    def get_input_data(self, obj):
        if self._can_view_data(obj):
            return obj.test_case.input_data
        return "[Hidden Test Case]"

    def get_expected_output(self, obj):
        if self._can_view_data(obj):
            return obj.test_case.expected_output
        return "[Hidden Test Case]"

    def get_actual_output(self, obj):
        if self._can_view_data(obj):
            return obj.actual_output
        return ""


class SubmissionListOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    problem_id = serializers.IntegerField(source='problem.id')
    problem_title = serializers.CharField(source='problem.title')
    problem_slug = serializers.CharField(source='problem.slug')
    language = serializers.CharField()
    status = serializers.CharField()
    execution_time = serializers.FloatField(allow_null=True)
    memory_usage = serializers.IntegerField(allow_null=True)
    passed_test_cases_count = serializers.IntegerField()
    total_test_cases_count = serializers.IntegerField()
    is_sample_run = serializers.BooleanField()
    created_at = serializers.DateTimeField()


class SubmissionDetailOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    problem_id = serializers.IntegerField(source='problem.id')
    problem_title = serializers.CharField(source='problem.title')
    problem_slug = serializers.CharField(source='problem.slug')
    language = serializers.CharField()
    source_code = serializers.CharField()
    status = serializers.CharField()
    execution_time = serializers.FloatField(allow_null=True)
    memory_usage = serializers.IntegerField(allow_null=True)
    compile_output = serializers.CharField(allow_blank=True)
    error_message = serializers.CharField(allow_blank=True)
    passed_test_cases_count = serializers.IntegerField()
    total_test_cases_count = serializers.IntegerField()
    is_sample_run = serializers.BooleanField()
    results = SubmissionResultOutputSerializer(many=True, source='results.all')
    created_at = serializers.DateTimeField()

