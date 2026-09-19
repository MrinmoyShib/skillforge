import pytest
from rest_framework.test import APIClient
from apps.accounts.models import User, UserProfile
from apps.problems.models import Category, Problem, DifficultyXPConfig
from apps.progress.services.progress_services import record_problem_solved


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def student_user(db):
    user = User.objects.create_user(
        username="dash_student",
        email="dash_student@example.com",
        password="TestPassword123!"
    )
    UserProfile.objects.create(user=user, display_name="Dash Student")
    return user


@pytest.fixture
def setup_catalog(db):
    DifficultyXPConfig.objects.get_or_create(difficulty="easy", defaults={"xp_reward": 50})
    cat_arrays, _ = Category.objects.get_or_create(name="Arrays", slug="arrays", display_order=1)
    cat_strings, _ = Category.objects.get_or_create(name="Strings", slug="strings", display_order=2)

    prob1 = Problem.objects.create(
        title="Array Problem 1",
        slug="array-prob-1",
        description="First array problem",
        difficulty="easy",
        category=cat_arrays,
        challenge_level=1,
        is_published=True
    )
    prob2 = Problem.objects.create(
        title="Array Problem 2",
        slug="array-prob-2",
        description="Second array problem",
        difficulty="easy",
        category=cat_arrays,
        challenge_level=2,
        is_published=True
    )
    prob3 = Problem.objects.create(
        title="String Problem 1",
        slug="string-prob-1",
        description="First string problem",
        difficulty="easy",
        category=cat_strings,
        challenge_level=1,
        is_published=True
    )
    return {"cat_arrays": cat_arrays, "cat_strings": cat_strings, "prob1": prob1, "prob2": prob2, "prob3": prob3}


@pytest.mark.django_db
class TestDashboardAPI:
    def test_dashboard_unauthenticated_fails(self, api_client):
        res = api_client.get("/api/v1/dashboard/")
        assert res.status_code == 401

    def test_dashboard_payload_structure(self, api_client, student_user, setup_catalog):
        api_client.force_authenticate(user=student_user)
        res = api_client.get("/api/v1/dashboard/")
        assert res.status_code == 200
        data = res.json()

        assert "stats" in data
        assert "category_mastery" in data
        assert "recent_submissions" in data
        assert "recommended_problems" in data
        assert "recent_activity" in data

        assert data["stats"]["username"] == "dash_student"
        assert len(data["category_mastery"]) >= 2
        assert len(data["recommended_problems"]) == 3

    def test_dashboard_category_mastery_and_recommendations(self, api_client, student_user, setup_catalog):
        api_client.force_authenticate(user=student_user)

        # Solve prob1 (in Arrays)
        record_problem_solved(
            user=student_user,
            problem=setup_catalog["prob1"],
            submission=None
        )

        res = api_client.get("/api/v1/dashboard/")
        assert res.status_code == 200
        data = res.json()

        # Check stats updated
        assert data["stats"]["problems_solved_count"] == 1
        assert data["stats"]["total_xp"] == 50

        # Check category mastery for Arrays: 1 of 2 solved = 50.0%
        arrays_mastery = next(c for c in data["category_mastery"] if c["slug"] == "arrays")
        assert arrays_mastery["total_problems"] == 2
        assert arrays_mastery["solved_problems"] == 1
        assert arrays_mastery["remaining_problems"] == 1
        assert arrays_mastery["xp_earned"] == 50
        assert arrays_mastery["mastery_percent"] == 50.0

        # Check recommended problems no longer contains prob1
        rec_ids = [p["id"] for p in data["recommended_problems"]]
        assert setup_catalog["prob1"].id not in rec_ids
        assert setup_catalog["prob3"].id in rec_ids or setup_catalog["prob2"].id in rec_ids

        # Check activity timeline contains the solve event
        assert len(data["recent_activity"]) >= 1
        assert "Array Problem 1" in data["recent_activity"][0]["description"]

