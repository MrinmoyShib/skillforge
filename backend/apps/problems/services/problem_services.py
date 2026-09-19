"""
Services (writes & mutations) for Problem and TestCase management.
"""
from typing import Optional, List, Dict, Any
from django.db import transaction
from ..models import Problem, Category, Tag, TestCase, DifficultyXPConfig

DEFAULT_XP_REWARDS = {
    Problem.DIFFICULTY_EASY: 50,
    Problem.DIFFICULTY_MEDIUM: 100,
    Problem.DIFFICULTY_HARD: 200,
}


def get_default_xp_reward(difficulty: str) -> int:
    config = DifficultyXPConfig.objects.filter(difficulty=difficulty).first()
    if config:
        return config.xp_reward
    return DEFAULT_XP_REWARDS.get(difficulty, 50)


def problem_create(
    *,
    title: str,
    description: str,
    difficulty: str,
    challenge_level: int = 1,
    category_id: int,
    tag_ids: Optional[List[int]] = None,
    xp_reward: Optional[int] = None,
    constraints: str = "",
    input_format: str = "",
    output_format: str = "",
    examples: Optional[List[Dict[str, Any]]] = None,
    starter_code: str = "",
    language: str = "cpp",
    time_limit_seconds: float = 2.0,
    memory_limit_kb: int = 262144,
    is_published: bool = False
) -> Problem:
    """
    Creates a new problem and associates tags atomically.
    """
    if xp_reward is None or xp_reward <= 0:
        xp_reward = get_default_xp_reward(difficulty)

    category = Category.objects.get(id=category_id)

    with transaction.atomic():
        problem = Problem.objects.create(
            title=title,
            description=description,
            difficulty=difficulty,
            challenge_level=challenge_level,
            category=category,
            xp_reward=xp_reward,
            constraints=constraints,
            input_format=input_format,
            output_format=output_format,
            examples=examples or [],
            starter_code=starter_code,
            language=language,
            time_limit_seconds=time_limit_seconds,
            memory_limit_kb=memory_limit_kb,
            is_published=is_published,
        )

        if tag_ids:
            problem.tags.set(tag_ids)

        return problem


def problem_update(
    *,
    problem: Problem,
    **data
) -> Problem:
    """
    Updates an existing problem.
    """
    with transaction.atomic():
        tag_ids = data.pop('tag_ids', None)
        category_id = data.pop('category_id', None)

        if category_id is not None:
            problem.category = Category.objects.get(id=category_id)

        for key, value in data.items():
            setattr(problem, key, value)

        problem.save()

        if tag_ids is not None:
            problem.tags.set(tag_ids)

        return problem


def problem_delete(*, problem: Problem) -> None:
    problem.delete()


def test_case_create(
    *,
    problem: Problem,
    input_data: str,
    expected_output: str,
    is_sample: bool = False,
    order: int = 0
) -> TestCase:
    return TestCase.objects.create(
        problem=problem,
        input_data=input_data,
        expected_output=expected_output,
        is_sample=is_sample,
        order=order
    )


def test_case_update(
    *,
    test_case: TestCase,
    **data
) -> TestCase:
    for key, value in data.items():
        setattr(test_case, key, value)
    test_case.save()
    return test_case


def test_case_delete(*, test_case: TestCase) -> None:
    test_case.delete()

