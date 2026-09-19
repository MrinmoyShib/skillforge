import pytest
from rest_framework.test import APIClient
from apps.accounts.models import User, UserProfile
from apps.problems.models import Category, Problem, DifficultyXPConfig
from apps.achievements.models import Achievement, UserAchievement
from apps.achievements.services.achievement_engine import check_and_grant_achievements
from apps.progress.services.progress_services import record_problem_solved


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def student_user(db):
    user = User.objects.create_user(
        username="ach_student",
        email="ach_student@example.com",
        password="TestPassword123!"
    )
    UserProfile.objects.create(user=user, display_name="Achievement Student")
    return user


@pytest.fixture
def seed_achievements_fixture(db):
    first_blood, _ = Achievement.objects.get_or_create(
        slug="first-blood",
        defaults={
            "name": "First Blood",
            "description": "Solve first problem",
            "icon": "⚔️",
            "criteria_type": Achievement.CriteriaType.FIRST_SOLVE,
            "criteria_value": 1,
            "xp_bonus": 25
        }
    )
    solver, _ = Achievement.objects.get_or_create(
        slug="problem-solver",
        defaults={
            "name": "Problem Solver",
            "description": "Solve 5 problems",
            "icon": "💡",
            "criteria_type": Achievement.CriteriaType.PROBLEMS_COUNT,
            "criteria_value": 5,
            "xp_bonus": 50
        }
    )
    return {"first_blood": first_blood, "solver": solver}


@pytest.fixture
def sample_problem(db):
    DifficultyXPConfig.objects.get_or_create(difficulty="easy", defaults={"xp_reward": 50})
    category, _ = Category.objects.get_or_create(name="Logic", slug="logic")
    return Problem.objects.create(
        title="Ach Test Problem",
        slug="ach-test-problem",
        description="Testing achievements",
        difficulty="easy",
        category=category,
        challenge_level=1,
        is_published=True
    )


@pytest.mark.django_db
class TestAchievementsAPI:
    def test_list_achievements_unauthenticated(self, api_client, seed_achievements_fixture):
        res = api_client.get("/api/v1/achievements/")
        assert res.status_code == 200
        data = res.json()
        assert len(data) >= 2
        assert all(item["is_unlocked"] is False for item in data)

    def test_first_blood_granted_on_first_solve(self, student_user, sample_problem, seed_achievements_fixture):
        # Initial: no achievements
        assert UserAchievement.objects.filter(user=student_user).count() == 0

        # Solve problem
        record_problem_solved(user=student_user, problem=sample_problem, submission=None)

        # Check First Blood granted
        grants = list(UserAchievement.objects.filter(user=student_user))
        assert len(grants) == 1
        assert grants[0].achievement.slug == "first-blood"

        # Check bonus XP applied (50 base + 25 bonus = 75)
        student_user.profile.refresh_from_db()
        assert student_user.profile.total_xp == 75

    def test_anti_duplicate_achievement_grant(self, student_user, seed_achievements_fixture):
        student_user.profile.problems_solved_count = 1
        student_user.profile.save()

        granted_first = check_and_grant_achievements(student_user)
        assert len(granted_first) == 1
        assert granted_first[0].slug == "first-blood"

        # Second check: already earned, must return empty
        granted_second = check_and_grant_achievements(student_user)
        assert len(granted_second) == 0
        assert UserAchievement.objects.filter(user=student_user).count() == 1

