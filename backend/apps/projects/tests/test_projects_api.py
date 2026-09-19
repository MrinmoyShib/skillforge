import pytest
from rest_framework.test import APIClient
from apps.accounts.models import User, UserProfile
from apps.projects.models import Project, ProjectMilestone, UserProjectProgress


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def student_user(db):
    user = User.objects.create_user(
        username="project_student",
        email="project_student@example.com",
        password="TestPassword123!"
    )
    UserProfile.objects.create(user=user, display_name="Project Student")
    return user


@pytest.fixture
def sample_project(db):
    project = Project.objects.create(
        title="Test Router",
        slug="test-router",
        language="python",
        difficulty="easy",
        challenge_level=1,
        short_description="A test router project",
        description="Full markdown description",
        technologies=["Python", "Regex"],
        xp_reward=100,
        estimated_minutes=30,
        is_published=True,
    )
    m1 = ProjectMilestone.objects.create(
        project=project,
        order=1,
        title="Milestone 1",
        description="Implement simple add function",
        starter_code="def add(a, b):\n    return 0",
        test_harness_code="assert add(2, 3) == 5\nprint('PASS')",
        xp_reward=50
    )
    m2 = ProjectMilestone.objects.create(
        project=project,
        order=2,
        title="Milestone 2",
        description="Implement subtract function",
        starter_code="def sub(a, b):\n    return 0",
        test_harness_code="assert sub(5, 3) == 2\nprint('PASS')",
        xp_reward=50
    )
    return project


@pytest.mark.django_db
class TestProjectsAPI:
    def test_list_projects(self, api_client, sample_project):
        res = api_client.get("/api/v1/projects/")
        assert res.status_code == 200
        data = res.json()
        assert len(data) >= 1
        p = next(x for x in data if x["slug"] == "test-router")
        assert p["title"] == "Test Router"
        assert p["milestones_count"] == 2
        assert p["user_status"] == "NOT_STARTED"

    def test_project_detail(self, api_client, sample_project):
        res = api_client.get(f"/api/v1/projects/{sample_project.slug}/")
        assert res.status_code == 200
        data = res.json()
        assert data["slug"] == "test-router"
        assert len(data["milestones"]) == 2
        assert data["milestones"][0]["order"] == 1

    def test_start_project(self, api_client, student_user, sample_project):
        api_client.force_authenticate(user=student_user)
        res = api_client.post(f"/api/v1/projects/{sample_project.slug}/start/")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "IN_PROGRESS"
        assert data["current_milestone_order"] == 1

    def test_verify_milestone_fail(self, api_client, student_user, sample_project):
        api_client.force_authenticate(user=student_user)
        m1 = sample_project.milestones.first()

        # Submit wrong code
        res = api_client.post(
            f"/api/v1/projects/{sample_project.slug}/milestones/{m1.id}/verify/",
            {"source_code": "# force_wrong_answer\ndef add(a, b):\n    return a - b"}
        )
        assert res.status_code == 200
        data = res.json()
        assert data["passed"] is False
        assert data["xp_awarded"] == 0

    def test_verify_milestone_pass_and_complete_project(self, api_client, student_user, sample_project):
        api_client.force_authenticate(user=student_user)
        m1 = sample_project.milestones.get(order=1)
        m2 = sample_project.milestones.get(order=2)

        # 1. Pass Milestone 1
        res1 = api_client.post(
            f"/api/v1/projects/{sample_project.slug}/milestones/{m1.id}/verify/",
            {"source_code": "def add(a, b):\n    return a + b"}
        )
        assert res1.status_code == 200
        d1 = res1.json()
        assert d1["passed"] is True
        assert d1["xp_awarded"] == 50
        assert d1["project_completed"] is False

        # 2. Pass Milestone 2 -> completes project (50 XP milestone + 100 XP project bonus)
        res2 = api_client.post(
            f"/api/v1/projects/{sample_project.slug}/milestones/{m2.id}/verify/",
            {"source_code": "def sub(a, b):\n    return a - b"}
        )
        assert res2.status_code == 200
        d2 = res2.json()
        assert d2["passed"] is True
        assert d2["xp_awarded"] == 150  # 50 + 100
        assert d2["project_completed"] is True

        # Verify UserProjectProgress is completed
        up = UserProjectProgress.objects.get(user=student_user, project=sample_project)
        assert up.status == "COMPLETED"
        assert len(up.completed_milestones) == 2
