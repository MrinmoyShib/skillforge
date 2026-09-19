import pytest
from datetime import timedelta
from django.utils import timezone
from rest_framework.test import APIClient
from apps.accounts.models import User, UserProfile
from apps.problems.models import Category, Problem, DifficultyXPConfig
from apps.submissions.models import Submission, SubmissionStatus
from apps.progress.models import LevelRequirement, UserProgress, ActivityLog
from apps.progress.services.progress_services import record_problem_solved
from apps.progress.services.leveling import calculate_level


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def student_user(db):
    user = User.objects.create_user(
        username="progress_student",
        email="student_prog@example.com",
        password="TestPassword123!"
    )
    UserProfile.objects.create(user=user, display_name="Progress Student")
    return user


@pytest.fixture
def sample_problem(db):
    DifficultyXPConfig.objects.get_or_create(difficulty="easy", defaults={"xp_reward": 50})
    category, _ = Category.objects.get_or_create(name="Algorithms", slug="algorithms")
    return Problem.objects.create(
        title="Test Prog Problem",
        slug="test-prog-problem",
        description="A problem for testing progress",
        difficulty="easy",
        category=category,
        challenge_level=1,
        is_published=True
    )


@pytest.mark.django_db
class TestProgressAPI:
    def test_unauthenticated_progress_fails(self, api_client):
        res = api_client.get("/api/v1/progress/")
        assert res.status_code == 401

    def test_get_user_progress_summary(self, api_client, student_user):
        api_client.force_authenticate(user=student_user)
        res = api_client.get("/api/v1/progress/")
        assert res.status_code == 200
        data = res.json()
        assert data["username"] == "progress_student"
        assert data["current_level"] == 1
        assert data["total_xp"] == 0
        assert data["problems_solved_count"] == 0

    def test_anti_farming_db_constraint(self, student_user, sample_problem):
        # 1. First solve
        xp_first = record_problem_solved(
            user=student_user,
            problem=sample_problem,
            submission=None
        )
        assert xp_first == 50
        student_user.profile.refresh_from_db()
        assert student_user.profile.total_xp == 50
        assert student_user.profile.problems_solved_count == 1

        # 2. Duplicate solve — MUST return 0 and not grant XP
        xp_second = record_problem_solved(
            user=student_user,
            problem=sample_problem,
            submission=None
        )
        assert xp_second == 0
        student_user.profile.refresh_from_db()
        assert student_user.profile.total_xp == 50
        assert student_user.profile.problems_solved_count == 1

    def test_level_calculation_thresholds(self, db):
        LevelRequirement.objects.update_or_create(level=1, defaults={"xp_threshold": 0, "title": "Apprentice"})
        LevelRequirement.objects.update_or_create(level=2, defaults={"xp_threshold": 100, "title": "Junior Coder"})

        res1 = calculate_level(50)
        assert res1["level"] == 1
        assert res1["title"] == "Apprentice"
        assert res1["progress_percent"] == 50.0

        res2 = calculate_level(150)
        assert res2["level"] == 2
        assert res2["title"] == "Junior Coder"

    def test_solved_problems_endpoint(self, api_client, student_user, sample_problem):
        api_client.force_authenticate(user=student_user)

        # Before solve
        res_before = api_client.get("/api/v1/progress/problems/")
        assert res_before.status_code == 200
        assert res_before.json()["solved_problem_ids"] == []

        # Record solve
        record_problem_solved(user=student_user, problem=sample_problem, submission=None)

        # After solve
        res_after = api_client.get("/api/v1/progress/problems/")
        assert res_after.status_code == 200
        data = res_after.json()
        assert data["total_solved"] == 1
        assert sample_problem.id in data["solved_problem_ids"]

    def test_streak_calculation(self, student_user, sample_problem):
        profile = student_user.profile
        profile.last_solve_date = timezone.now().date() - timedelta(days=1)
        profile.current_streak_days = 2
        profile.save()

        record_problem_solved(user=student_user, problem=sample_problem, submission=None)
        profile.refresh_from_db()

        assert profile.current_streak_days == 3
        assert profile.last_solve_date == timezone.now().date()

