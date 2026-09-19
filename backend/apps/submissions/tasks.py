"""
Celery asynchronous task for executing and grading code submissions.
"""
import logging
from celery import shared_task
from django.db import transaction
from django.utils import timezone
from apps.problems.models import TestCase
from .models import Submission, SubmissionResult, SubmissionStatus
from .engine import get_execution_engine

logger = logging.getLogger(__name__)


def award_xp_and_update_profile(submission):
    """
    Awards XP to user profile only if this is their first Accepted solve on this problem.
    Guarantees anti-farming rule (§10.4) using apps.progress.
    """
    from apps.progress.services.progress_services import record_problem_solved
    return record_problem_solved(
        user=submission.user,
        problem=submission.problem,
        submission=submission
    )


@shared_task(bind=True, max_retries=1, time_limit=120, soft_time_limit=90)
def evaluate_submission_task(self, submission_id: int):
    """
    Executes a submission against target test cases inside the sandbox runner.
    """
    try:
        submission = Submission.objects.select_related('user', 'problem').get(id=submission_id)
    except Submission.DoesNotExist:
        logger.error(f"Submission {submission_id} not found.")
        return

    try:
        submission.status = SubmissionStatus.PROCESSING
        submission.save(update_fields=['status'])

        problem = submission.problem
        if submission.is_sample_run:
            test_cases = list(TestCase.objects.filter(problem=problem, is_sample=True).order_by('order', 'id'))
        else:
            test_cases = list(TestCase.objects.filter(problem=problem).order_by('order', 'id'))

        submission.total_test_cases_count = len(test_cases)
        submission.passed_test_cases_count = 0
        submission.save(update_fields=['total_test_cases_count', 'passed_test_cases_count'])

        if not test_cases:
            # Edge case: no test cases defined
            submission.status = SubmissionStatus.INTERNAL_ERROR
            submission.error_message = 'Problem has no test cases configured.'
            submission.save(update_fields=['status', 'error_message'])
            return

        engine = get_execution_engine()

        overall_status = SubmissionStatus.ACCEPTED
        max_exec_time = 0.0
        max_memory = 0
        compile_output = ""
        error_message = ""

        # Clean old results if re-evaluating
        SubmissionResult.objects.filter(submission=submission).delete()
        
        results_list = []

        for tc in test_cases:
            res = engine.execute(
                source_code=submission.source_code,
                language=submission.language,
                stdin=tc.input_data,
                expected_output=tc.expected_output,
                time_limit=problem.time_limit_seconds,
                memory_limit=problem.memory_limit_kb
            )

            # Track resource usage
            if res.execution_time and res.execution_time > max_exec_time:
                max_exec_time = res.execution_time
            if res.memory_usage and res.memory_usage > max_memory:
                max_memory = res.memory_usage
            if res.compile_output:
                compile_output = res.compile_output
            if res.error_message:
                error_message = res.error_message

            # Record individual test case result in list
            results_list.append(
                SubmissionResult(
                    submission=submission,
                    test_case=tc,
                    status=res.status,
                    execution_time=res.execution_time,
                    memory_usage=res.memory_usage,
                    actual_output=res.stdout,
                    stderr_output=res.stderr,
                    order=tc.order
                )
            )

            if res.status == SubmissionStatus.ACCEPTED:
                submission.passed_test_cases_count += 1
            else:
                # First failure dictates the overall submission status
                if overall_status == SubmissionStatus.ACCEPTED:
                    overall_status = res.status

                # If compilation failed, all other test cases will fail identically — abort loop early
                if res.status == SubmissionStatus.COMPILATION_ERROR:
                    break
        
        # Bulk create all results
        SubmissionResult.objects.bulk_create(results_list)

        # Finalize submission
        submission.status = overall_status
        submission.execution_time = round(max_exec_time, 3)
        submission.memory_usage = max_memory
        submission.compile_output = compile_output
        submission.error_message = error_message
        submission.save()

        # If accepted on a full run, award XP
        if overall_status == SubmissionStatus.ACCEPTED and not submission.is_sample_run:
            award_xp_and_update_profile(submission)

        logger.info(f"Submission {submission_id} evaluated with verdict {overall_status} ({submission.passed_test_cases_count}/{submission.total_test_cases_count} passed).")
        return {
            "submission_id": submission_id,
            "status": overall_status,
            "passed": submission.passed_test_cases_count,
            "total": submission.total_test_cases_count
        }
    except Exception as e:
        submission.status = SubmissionStatus.INTERNAL_ERROR
        submission.error_message = str(e)
        submission.save(update_fields=['status', 'error_message'])
        return {
            "submission_id": submission_id,
            "status": submission.status,
            "error": str(e)
        }
