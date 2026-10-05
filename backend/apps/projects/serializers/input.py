"""
Input validation serializers for Guided Projects.
"""
from rest_framework import serializers


class ProjectFilterInputSerializer(serializers.Serializer):
    language = serializers.ChoiceField(choices=['python', 'javascript', 'cpp'], required=False)
    difficulty = serializers.ChoiceField(choices=['easy', 'medium', 'hard'], required=False)
    search = serializers.CharField(required=False, allow_blank=True)
    status = serializers.ChoiceField(choices=['NOT_STARTED', 'IN_PROGRESS', 'COMPLETED'], required=False)


class MilestoneVerifyInputSerializer(serializers.Serializer):
    source_code = serializers.CharField(
        min_length=1,
        max_length=65536,
        help_text="Student's implementation code for the milestone",
        error_messages={"max_length": "Source code cannot exceed 64 KB."}
    )

