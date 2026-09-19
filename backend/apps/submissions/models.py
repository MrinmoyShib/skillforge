"""
Models for Submissions and Test Case Execution Results.
"""
from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel
from apps.problems.models import Problem, TestCase


class SubmissionStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    PROCESSING = 'PROCESSING', 'Processing'
    ACCEPTED = 'ACCEPTED', 'Accepted'
    WRONG_ANSWER = 'WRONG_ANSWER', 'Wrong Answer'
    COMPILATION_ERROR = 'COMPILATION_ERROR', 'Compilation Error'
    RUNTIME_ERROR = 'RUNTIME_ERROR', 'Runtime Error'
    TIME_LIMIT_EXCEEDED = 'TIME_LIMIT_EXCEEDED', 'Time Limit Exceeded'
    MEMORY_LIMIT_EXCEEDED = 'MEMORY_LIMIT_EXCEEDED', 'Memory Limit Exceeded'
    INTERNAL_ERROR = 'INTERNAL_ERROR', 'Internal Error'


class Submission(TimeStampedModel):
    """
    Code submission record for a user against a specific problem.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='submissions')
    language = models.CharField(max_length=50, default='cpp')
    source_code = models.TextField()
    status = models.CharField(
        max_length=30,
        choices=SubmissionStatus.choices,
        default=SubmissionStatus.PENDING,
        db_index=True
    )
    execution_time = models.FloatField(null=True, blank=True, help_text="Execution time in seconds (max across test cases)")
    memory_usage = models.PositiveIntegerField(null=True, blank=True, help_text="Memory usage in KB (max across test cases)")
    compile_output = models.TextField(blank=True, help_text="Compiler stderr or diagnostic output")
    error_message = models.TextField(blank=True, help_text="System error or evaluation failure message")
    passed_test_cases_count = models.PositiveIntegerField(default=0)
    total_test_cases_count = models.PositiveIntegerField(default=0)
    is_sample_run = models.BooleanField(default=False, db_index=True, help_text="True if run only against public sample test cases")

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['problem', '-created_at']),
            models.Index(fields=['status', '-created_at']),
        ]

    def __str__(self):
        return f"Submission #{self.id} — {self.user.username} on {self.problem.title} [{self.status}]"


class SubmissionResult(TimeStampedModel):
    """
    Evaluation verdict and telemetry for a single test case run.
    """
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='results')
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE, related_name='submission_results')
    status = models.CharField(max_length=30, choices=SubmissionStatus.choices)
    execution_time = models.FloatField(null=True, blank=True, help_text="Runtime in seconds")
    memory_usage = models.PositiveIntegerField(null=True, blank=True, help_text="Memory in KB")
    actual_output = models.TextField(blank=True, help_text="Captured standard output")
    stderr_output = models.TextField(blank=True, help_text="Captured standard error")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"Result #{self.id} for Submission #{self.submission_id} (Case #{self.test_case_id}): {self.status}"

