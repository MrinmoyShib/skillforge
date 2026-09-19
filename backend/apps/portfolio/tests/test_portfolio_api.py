import pytest
from rest_framework.test import APIClient
from apps.accounts.models import User, UserProfile
from apps.problems.models import Category, Problem, Tag
from apps.progress.models import UserProgress, ActivityLog
from apps.projects.models import Project, UserProjectProgress
from apps.achievements.models import Achievement, UserAchievement
from django.utils import timezone


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def portfolio_user(db):
    user = User.objects.create_user(
        username="dev_showcase",
        email="dev_showcase@example.com",
        password="TestPassword123!"
    )
    profile = UserProfile.objects.create(
        user=user,
        display_name="Dev Showcase",
        total_xp=250,
        problems_solved_count=3,
        current_streak_days=5,
        bio="Full-stack engineer & algorithmic problem solver.",
    )

    # Category and Problem
    cat_py = Category.objects.create(name="Python Track", slug="python", display_order=1)
    tag_arrays = Tag.objects.create(name="Arrays", slug="arrays")

    prob = Problem.objects.create(
        title="Sample Problem",
        slug="sample-problem",
        category=cat_py,
        difficulty="easy",
        challenge_level=1,
        xp_reward=50,
        is_published=True,
    )
    prob.tags.add(tag_arrays)

    # User progress
    UserProgress.objects.create(
        user=user,
        problem=prob,
        solved=True,
        first_solved_at=timezone.now(),
        xp_awarded=50,
    )

    # Project and UserProjectProgress
    project = Project.objects.create(
        title="Async Task Queue",
        slug="async-task-queue",
        language="python",
        difficulty="medium",
        challenge_level=2,
        short_description="Persistent task queue",
        description="Detailed description",
        technologies=["Python", "Redis"],
        xp_reward=150,
        is_published=True,
    )
    UserProjectProgress.objects.create(
        user=user,
        project=project,
        status="COMPLETED",
        completed_milestones=[1, 2],
        completed_at=timezone.now(),
    )

    # Achievement
    ach = Achievement.objects.create(
        name="First Blood",
        slug="first-solve",
        description="Solved first problem",
        icon="⚔️",
        criteria_type=Achievement.CriteriaType.FIRST_SOLVE,
        criteria_value=1,
        xp_bonus=50,
    )
    UserAchievement.objects.create(
        user=user,
        achievement=ach,
        earned_at=timezone.now(),
    )

    # Activity Log
    ActivityLog.objects.create(
        user=user,
        activity_type=ActivityLog.ActivityType.SOLVE,
        description="Solved Sample Problem",
    )

    return user


@pytest.mark.django_db
class TestPortfolioAPI:
    def test_get_public_portfolio_success(self, api_client, portfolio_user):
        res = api_client.get(f"/api/v1/portfolio/{portfolio_user.username}/")
        assert res.status_code == 200
        data = res.json()

        # Check user info
        assert data["user"]["username"] == "dev_showcase"
        assert data["user"]["display_name"] == "Dev Showcase"
        assert data["user"]["total_xp"] == 250
        assert data["user"]["current_streak_days"] == 5
        assert "github_url" in data["user"]

        # Check tracks
        assert len(data["tracks"]) >= 1
        py_track = next(t for t in data["tracks"] if t["slug"] == "python")
        assert py_track["solved_problems"] == 1
        assert py_track["xp_earned"] == 50

        # Check verified projects
        assert len(data["verified_projects"]) == 1
        assert data["verified_projects"][0]["slug"] == "async-task-queue"
        assert data["verified_projects"][0]["xp_reward"] == 150

        # Check skill domains
        assert len(data["skill_domains"]) >= 1
        assert data["skill_domains"][0]["slug"] == "arrays"

        # Check achievements
        assert len(data["achievements"]) == 1
        assert data["achievements"][0]["code"] == "first-solve"
        assert data["achievements"][0]["badge_type"] == "silver"

        # Check recent activity
        assert len(data["recent_activity"]) == 1
        assert "Solved Sample Problem" in data["recent_activity"][0]["description"]

    def test_get_public_portfolio_not_found(self, api_client):
        res = api_client.get("/api/v1/portfolio/nonexistent_dev_user/")
        assert res.status_code == 404
        data = res.json()
        assert "detail" in data
