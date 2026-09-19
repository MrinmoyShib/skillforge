"""
Input serializers for filtering, creating, and updating coding problems.
"""
from rest_framework import serializers
from ..models import Problem, Category, Tag


class ProblemFilterInputSerializer(serializers.Serializer):
    difficulty = serializers.ChoiceField(choices=Problem.DIFFICULTY_CHOICES, required=False)
    category = serializers.CharField(required=False, help_text="Category slug")
    level = serializers.IntegerField(min_value=1, max_value=5, required=False)
    search = serializers.CharField(required=False, max_length=100)
    ordering = serializers.ChoiceField(
        choices=['challenge_level', '-challenge_level', 'xp_reward', '-xp_reward', 'created_at', '-created_at'],
        default='challenge_level',
        required=False
    )


class ProblemCreateInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    difficulty = serializers.ChoiceField(choices=Problem.DIFFICULTY_CHOICES)
    challenge_level = serializers.IntegerField(min_value=1, max_value=5, default=1)
    category_id = serializers.IntegerField()
    tag_ids = serializers.ListField(child=serializers.IntegerField(), required=False, default=list)
    xp_reward = serializers.IntegerField(min_value=0, required=False)
    constraints = serializers.CharField(required=False, allow_blank=True, default='')
    input_format = serializers.CharField(required=False, allow_blank=True, default='')
    output_format = serializers.CharField(required=False, allow_blank=True, default='')
    examples = serializers.ListField(child=serializers.DictField(), required=False, default=list)
    starter_code = serializers.CharField(required=False, allow_blank=True, default='')
    language = serializers.CharField(max_length=50, default='cpp')
    time_limit_seconds = serializers.FloatField(default=2.0)
    memory_limit_kb = serializers.IntegerField(default=262144)
    is_published = serializers.BooleanField(default=False)

    def validate_category_id(self, value):
        if not Category.objects.filter(id=value).exists():
            raise serializers.ValidationError("Category does not exist.")
        return value

    def validate_tag_ids(self, value):
        existing_count = Tag.objects.filter(id__in=value).count()
        if existing_count != len(value):
            raise serializers.ValidationError("One or more tag IDs are invalid.")
        return value


class ProblemUpdateInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, required=False)
    description = serializers.CharField(required=False)
    difficulty = serializers.ChoiceField(choices=Problem.DIFFICULTY_CHOICES, required=False)
    challenge_level = serializers.IntegerField(min_value=1, max_value=5, required=False)
    category_id = serializers.IntegerField(required=False)
    tag_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    xp_reward = serializers.IntegerField(min_value=0, required=False)
    constraints = serializers.CharField(required=False, allow_blank=True)
    input_format = serializers.CharField(required=False, allow_blank=True)
    output_format = serializers.CharField(required=False, allow_blank=True)
    examples = serializers.ListField(child=serializers.DictField(), required=False)
    starter_code = serializers.CharField(required=False, allow_blank=True)
    language = serializers.CharField(max_length=50, required=False)
    time_limit_seconds = serializers.FloatField(required=False)
    memory_limit_kb = serializers.IntegerField(required=False)
    is_published = serializers.BooleanField(required=False)


class TestCaseCreateInputSerializer(serializers.Serializer):
    input_data = serializers.CharField(allow_blank=True)
    expected_output = serializers.CharField()
    is_sample = serializers.BooleanField(default=False)
    order = serializers.IntegerField(default=0)


class TestCaseUpdateInputSerializer(serializers.Serializer):
    input_data = serializers.CharField(required=False, allow_blank=True)
    expected_output = serializers.CharField(required=False)
    is_sample = serializers.BooleanField(required=False)
    order = serializers.IntegerField(required=False)

