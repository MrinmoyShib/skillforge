"""
Selectors (database queries) for problems, categories, tags, and test cases.
"""
from typing import Optional, Dict, Any
from django.db.models import QuerySet, Q, Count
from ..models import Problem, Category, Tag, TestCase


def problem_list(*, filters: Optional[Dict[str, Any]] = None, is_admin: bool = False) -> QuerySet[Problem]:
    """
    Returns filtered and sorted problems with related category and tags.
    Non-admins only see published problems.
    """
    qs = Problem.objects.select_related('category').prefetch_related('tags')

    if not is_admin:
        qs = qs.filter(is_published=True)

    if not filters:
        return qs

    if 'difficulty' in filters and filters['difficulty']:
        qs = qs.filter(difficulty=filters['difficulty'])

    if 'category' in filters and filters['category']:
        qs = qs.filter(category__slug=filters['category'])

    if 'level' in filters and filters['level']:
        qs = qs.filter(challenge_level=filters['level'])

    if 'search' in filters and filters['search']:
        term = filters['search'].strip()
        qs = qs.filter(Q(title__icontains=term) | Q(description__icontains=term))

    ordering = filters.get('ordering', 'challenge_level')
    return qs.order_by(ordering, 'id')


def problem_get_by_slug(*, slug: str, is_admin: bool = False) -> Optional[Problem]:
    """
    Returns a single problem by slug with its sample test cases preloaded.
    """
    qs = Problem.objects.select_related('category').prefetch_related('tags')
    if not is_admin:
        qs = qs.filter(is_published=True)

    problem = qs.filter(slug=slug).first()
    if problem:
        # Preload only sample test cases for public presentation
        problem.sample_test_cases = list(
            TestCase.objects.filter(problem=problem, is_sample=True).order_by('order', 'id')
        )
    return problem


def problem_get_by_id(*, problem_id: int) -> Optional[Problem]:
    """
    Returns a single problem by ID with full test cases (for admin & internal evaluation).
    """
    problem = Problem.objects.select_related('category').prefetch_related('tags').filter(id=problem_id).first()
    if problem:
        problem.test_cases_list = list(
            TestCase.objects.filter(problem=problem).order_by('order', 'id')
        )
    return problem


def category_list() -> QuerySet[Category]:
    """
    Returns categories annotated with the count of published problems.
    """
    return Category.objects.annotate(
        problem_count=Count('problems', filter=Q(problems__is_published=True))
    ).order_by('display_order', 'name')


def tag_list() -> QuerySet[Tag]:
    return Tag.objects.all().order_by('name')


def test_cases_for_problem(*, problem_id: int, only_samples: bool = False) -> QuerySet[TestCase]:
    """
    Returns test cases for a problem.
    """
    qs = TestCase.objects.filter(problem_id=problem_id).order_by('order', 'id')
    if only_samples:
        qs = qs.filter(is_sample=True)
    return qs

