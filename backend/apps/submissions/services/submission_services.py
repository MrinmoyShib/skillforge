"""
Services for creating and enqueueing submissions.
"""
from django.db import transaction
from apps.problems.models import Problem
from ..models import Submission, SubmissionStatus
from ..tasks import evaluate_submission_task


def submission_create(
    *,
    user,
    problem_id: int,
    source_code: str,
    language: str = 'cpp',
    is_sample_run: bool = False
) -> Submission:
    """
    Creates a new pending submission and enqueues Celery evaluation.
    """
    problem = Problem.objects.get(id=problem_id, is_published=True)

    with transaction.atomic():
        submission = Submission.objects.create(
            user=user,
            problem=problem,
            language=language,
            source_code=source_code,
            status=SubmissionStatus.PENDING,
            is_sample_run=is_sample_run,
        )

        # Enqueue evaluation task asynchronously after database transaction commits
        transaction.on_commit(lambda: evaluate_submission_task.delay(submission.id))

        return submission

