"""
Input serializers for creating and filtering code submissions.
"""
from rest_framework import serializers
from apps.problems.models import Problem
from ..models import SubmissionStatus


LANGUAGE_CHOICES = ['python', 'javascript', 'cpp']


class SubmissionCreateInputSerializer(serializers.Serializer):
    problem_id = serializers.IntegerField()
    source_code = serializers.CharField(
        min_length=5,
        max_length=65536,
        help_text="User's solution source code",
        error_messages={"max_length": "Source code cannot exceed 64 KB."}
    )
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='cpp')
    is_sample_run = serializers.BooleanField(default=False, help_text="True to test against sample cases only")

    def validate_problem_id(self, value):
        if not Problem.objects.filter(id=value, is_published=True).exists():
            raise serializers.ValidationError("Problem does not exist or is not published.")
        return value

    def validate(self, attrs):
        problem_id = attrs.get('problem_id')
        language = attrs.get('language')
        if problem_id and language:
            try:
                problem = Problem.objects.get(id=problem_id)
                if problem.language and language != problem.language:
                    raise serializers.ValidationError({
                        "language": f"This challenge is designed for {problem.language.capitalize()} Track only."
                    })
            except Problem.DoesNotExist:
                pass
        return attrs


class SubmissionFilterInputSerializer(serializers.Serializer):
    problem_id = serializers.IntegerField(required=False)
    status = serializers.ChoiceField(choices=SubmissionStatus.choices, required=False)

