"""
Output presentation serializers for problems, test cases, and taxonomies.
"""
from rest_framework import serializers


class CategoryOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.CharField()
    description = serializers.CharField(allow_blank=True)
    display_order = serializers.IntegerField()
    problem_count = serializers.IntegerField(default=0, required=False)


class TagOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.CharField()


class SampleTestCaseOutputSerializer(serializers.Serializer):
    """
    Public test case serializer — strictly exposes only sample cases.
    """
    id = serializers.IntegerField()
    input_data = serializers.CharField()
    expected_output = serializers.CharField()
    is_sample = serializers.BooleanField()
    order = serializers.IntegerField()


class AdminTestCaseOutputSerializer(serializers.Serializer):
    """
    Admin-only test case serializer — includes hidden test cases.
    """
    id = serializers.IntegerField()
    problem_id = serializers.IntegerField()
    input_data = serializers.CharField()
    expected_output = serializers.CharField()
    is_sample = serializers.BooleanField()
    order = serializers.IntegerField()
    created_at = serializers.DateTimeField()


class ProblemListOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    slug = serializers.CharField()
    language = serializers.CharField(default='cpp')
    difficulty = serializers.CharField()
    challenge_level = serializers.IntegerField()
    xp_reward = serializers.IntegerField()
    category = CategoryOutputSerializer()
    tags = TagOutputSerializer(many=True)
    is_published = serializers.BooleanField()
    created_at = serializers.DateTimeField()


class ProblemDetailOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    slug = serializers.CharField()
    description = serializers.CharField()
    difficulty = serializers.CharField()
    challenge_level = serializers.IntegerField()
    xp_reward = serializers.IntegerField()
    category = CategoryOutputSerializer()
    tags = TagOutputSerializer(many=True)
    constraints = serializers.CharField()
    input_format = serializers.CharField()
    output_format = serializers.CharField()
    examples = serializers.ListField()
    starter_code = serializers.CharField()
    language = serializers.CharField()
    time_limit_seconds = serializers.FloatField()
    memory_limit_kb = serializers.IntegerField()
    sample_test_cases = SampleTestCaseOutputSerializer(many=True)
    created_at = serializers.DateTimeField()


class AdminProblemDetailOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    slug = serializers.CharField()
    description = serializers.CharField()
    difficulty = serializers.CharField()
    challenge_level = serializers.IntegerField()
    xp_reward = serializers.IntegerField()
    category = CategoryOutputSerializer()
    tags = TagOutputSerializer(many=True)
    constraints = serializers.CharField()
    input_format = serializers.CharField()
    output_format = serializers.CharField()
    examples = serializers.ListField()
    starter_code = serializers.CharField()
    language = serializers.CharField()
    time_limit_seconds = serializers.FloatField()
    memory_limit_kb = serializers.IntegerField()
    is_published = serializers.BooleanField()
    test_cases = AdminTestCaseOutputSerializer(many=True, source='test_cases.all')
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
