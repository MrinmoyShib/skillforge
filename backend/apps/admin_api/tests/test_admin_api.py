"""
Unit tests for the Admin Backoffice REST API.
"""
import pytest
from rest_framework.test import APIClient
from apps.accounts.models import User, UserProfile
from apps.problems.models import Problem, Category, TestCase
from apps.submissions.models import Submission, SubmissionStatus
from apps.projects.models import Project, ProjectMilestone


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user(db):
    user = User.objects.create_superuser(
        username='testadmin',
        email='admin@test.com',
        password='AdminPassword123!'
    )
    UserProfile.objects.get_or_create(user=user, defaults={'display_name': 'Test Admin'})
    return user


@pytest.fixture
def student_user(db):
    user = User.objects.create_user(
        username='teststudent',
        email='student@test.com',
        password='StudentPassword123!'
    )
    UserProfile.objects.get_or_create(user=user, defaults={'display_name': 'Test Student', 'total_xp': 100})
    return user


@pytest.fixture
def sample_problem(db):
    cat, _ = Category.objects.get_or_create(name='Algorithms', slug='algorithms')
    prob = Problem.objects.create(
        title='Sample Admin Test Problem',
        slug='sample-admin-test-problem',
        description='Solve this test problem.',
        category=cat,
        difficulty='easy',
        challenge_level=1,
        language='python',
        is_published=True,
        xp_reward=50
    )
    TestCase.objects.create(
        problem=prob,
        input_data='5\n',
        expected_output='10\n',
        is_sample=True,
        order=1
    )
    return prob


@pytest.mark.django_db
def test_admin_analytics_permissions(api_client, student_user, admin_user):
    # Unauthenticated -> 401
    res = api_client.get('/api/v1/admin/analytics/')
    assert res.status_code == 401

    # Normal student -> 403
    api_client.force_authenticate(user=student_user)
    res = api_client.get('/api/v1/admin/analytics/')
    assert res.status_code == 403

    # Admin user -> 200
    api_client.force_authenticate(user=admin_user)
    res = api_client.get('/api/v1/admin/analytics/')
    assert res.status_code == 200
    assert 'total_users' in res.data
    assert 'total_problems' in res.data
    assert 'system_health' in res.data
    assert res.data['system_health']['database'] == 'healthy'


@pytest.mark.django_db
def test_admin_problem_crud(api_client, admin_user, sample_problem):
    api_client.force_authenticate(user=admin_user)

    # List problems
    res = api_client.get('/api/v1/admin/problems/')
    assert res.status_code == 200
    assert len(res.data['results']) >= 1

    import uuid
    unique_slug = f"created-by-admin-{uuid.uuid4().hex[:6]}"

    # Create problem
    payload = {
        "title": "Created by Admin",
        "slug": unique_slug,
        "description": "Admin created challenge.",
        "difficulty": "medium",
        "challenge_level": 2,
        "language": "python",
        "xp_reward": 75,
        "is_published": False,
        "category_slug": "algorithms",
        "test_cases": [
            {
                "input_data": "1 2\n",
                "expected_output": "3\n",
                "is_sample": True,
                "order": 1
            }
        ]
    }
    create_res = api_client.post('/api/v1/admin/problems/', payload, format='json')
    if create_res.status_code != 201:
        print("CREATE_RES ERROR:", create_res.data)
    assert create_res.status_code == 201
    prob_id = create_res.data['id']

    # Retrieve problem
    detail_res = api_client.get(f'/api/v1/admin/problems/{prob_id}/')
    assert detail_res.status_code == 200
    assert detail_res.data['title'] == "Created by Admin"
    assert len(detail_res.data['test_cases']) == 1

    # Update problem (publish it)
    update_res = api_client.patch(f'/api/v1/admin/problems/{prob_id}/', {'is_published': True}, format='json')
    assert update_res.status_code == 200
    assert update_res.data['is_published'] is True

    # Delete problem
    delete_res = api_client.delete(f'/api/v1/admin/problems/{prob_id}/')
    assert delete_res.status_code == 204


@pytest.mark.django_db
def test_admin_verify_solution(api_client, admin_user, sample_problem):
    api_client.force_authenticate(user=admin_user)

    # Correct solution: reads 5 and outputs 10
    correct_code = "n = int(input())\nprint(n * 2)\n"
    res = api_client.post(
        f'/api/v1/admin/problems/{sample_problem.id}/verify/',
        {'source_code': correct_code, 'language': 'python'},
        format='json'
    )
    assert res.status_code == 200
    assert res.data['all_passed'] is True
    assert res.data['passed_count'] == 1

    # Wrong solution using force_wrong_answer marker
    wrong_code = "# force_wrong_answer\nprint(0)\n"
    res_wrong = api_client.post(
        f'/api/v1/admin/problems/{sample_problem.id}/verify/',
        {'source_code': wrong_code, 'language': 'python'},
        format='json'
    )
    assert res_wrong.status_code == 200
    assert res_wrong.data['all_passed'] is False


@pytest.mark.django_db
def test_admin_user_management_and_adjust_xp(api_client, admin_user, student_user):
    api_client.force_authenticate(user=admin_user)

    # List users
    res = api_client.get('/api/v1/admin/users/')
    assert res.status_code == 200

    # User detail
    detail_res = api_client.get(f'/api/v1/admin/users/{student_user.id}/')
    assert detail_res.status_code == 200
    assert detail_res.data['username'] == 'teststudent'
    assert 'track_breakdown' in detail_res.data

    # Adjust XP
    initial_xp = student_user.profile.total_xp
    xp_res = api_client.post(
        f'/api/v1/admin/users/{student_user.id}/adjust-xp/',
        {'xp_delta': 150, 'reason': 'Bonus for community contribution'},
        format='json'
    )
    assert xp_res.status_code == 200
    assert xp_res.data['total_xp'] == initial_xp + 150


@pytest.mark.django_db
def test_admin_submission_rejudge(api_client, admin_user, student_user, sample_problem):
    api_client.force_authenticate(user=admin_user)

    sub = Submission.objects.create(
        user=student_user,
        problem=sample_problem,
        language='python',
        source_code='n = int(input())\nprint(n * 2)\n',
        status=SubmissionStatus.PENDING
    )

    # List submissions
    res = api_client.get('/api/v1/admin/submissions/')
    assert res.status_code == 200

    # Rejudge submission
    rejudge_res = api_client.post(f'/api/v1/admin/submissions/{sub.id}/rejudge/')
    assert rejudge_res.status_code == 200
    assert rejudge_res.data['status'] == SubmissionStatus.ACCEPTED
