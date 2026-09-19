"""
Selectors (queries) for submissions and results.
"""
from typing import Optional, Dict, Any
from django.db.models import QuerySet
from ..models import Submission


def submission_list_for_user(*, user, filters: Optional[Dict[str, Any]] = None) -> QuerySet[Submission]:
    """
    Returns user's submissions with preloaded problem relation.
    """
    qs = Submission.objects.filter(user=user).select_related('problem')

    if filters:
        if 'problem_id' in filters and filters['problem_id']:
            qs = qs.filter(problem_id=filters['problem_id'])
        if 'status' in filters and filters['status']:
            qs = qs.filter(status=filters['status'])

    return qs.order_by('-created_at')


def submission_get_by_id(*, submission_id: int, user) -> Optional[Submission]:
    """
    Fetches a submission by ID, ensuring ownership unless user is staff.
    """
    qs = Submission.objects.select_related('problem').prefetch_related('results__test_case')
    if not user.is_staff:
        qs = qs.filter(user=user)

    return qs.filter(id=submission_id).first()

