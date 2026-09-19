"""
Input serializers for creating and filtering code submissions.
"""
from rest_framework import serializers
from apps.problems.models import Problem
from ..models import SubmissionStatus


class SubmissionCreateInputSerializer(serializers.Serializer):
    problem_id = serializers.IntegerField()
    source_code = serializers.CharField(min_length=5, help_text="User's solution source code")
    language = serializers.CharField(default='cpp', max_length=50)
    is_sample_run = serializers.BooleanField(default=False, help_text="True to test against sample cases only")

    def validate_problem_id(self, value):
        if not Problem.objects.filter(id=value, is_published=True).exists():
            raise serializers.ValidationError("Problem does not exist or is not published.")
        return value


class SubmissionFilterInputSerializer(serializers.Serializer):
    problem_id = serializers.IntegerField(required=False)
    status = serializers.ChoiceField(choices=SubmissionStatus.choices, required=False)

